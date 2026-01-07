
import zipfile
import shutil
import os
import json
import sys
from lxml import etree
from difflib import unified_diff
from pathlib import Path

# Namespaces
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
}
XML_SPACE = "{http://www.w3.org/XML/1998/namespace}space"

# Correct namespace for .rels file
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
def REL(tag):
    return f"{{{REL_NS}}}{tag}"


# ---------- helper: preserve spaces ----------
def set_text_preserve(t_el, text):
    t_el.text = text
    t_el.set(XML_SPACE, "preserve")


# ---------- helper: extract visible text for diff ----------
def extract_docx_text(docx_path):
    with zipfile.ZipFile(docx_path, "r") as z:
        xml = z.read("word/document.xml")

    root = etree.fromstring(xml)
    paragraphs = []
    for p in root.findall(".//w:p", NS):
        pieces = []
        for t in p.findall(".//w:t", NS):
            pieces.append(t.text or "")
        paragraphs.append("".join(pieces))
    return paragraphs


def compare_docs(original, modified, report_file):
    orig = extract_docx_text(original)
    mod = extract_docx_text(modified)

    orig_clean = [p.rstrip("\n") for p in orig]
    mod_clean = [p.rstrip("\n") for p in mod]

    diff = list(unified_diff(
        orig_clean,
        mod_clean,
        fromfile="ORIGINAL",
        tofile="MODIFIED",
        lineterm=""
    ))

    if not diff:
        print("\n[OK] No visible-text differences found.\n")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("No visible differences found.\n")
    else:
        print(f"\n[!] Visible differences found. See {report_file}\n")
        with open(report_file, "w", encoding="utf-8") as f:
            for line in diff:
                f.write(line + "\n")


# ---------- main hyperlink insertion ----------
def add_hyperlinks_to_docx(input_docx, output_docx, mapping_json):
    with open(mapping_json, "r", encoding="utf-8") as f:
        link_map = json.load(f)

    temp_dir = "docx_temp"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    # unzip
    with zipfile.ZipFile(input_docx, "r") as z:
        z.extractall(temp_dir)

    document_path = os.path.join(temp_dir, "word", "document.xml")
    rels_path = os.path.join(temp_dir, "word", "_rels", "document.xml.rels")

    tree = etree.parse(document_path)
    root = tree.getroot()

    rels_tree = etree.parse(rels_path)
    rels_root = rels_tree.getroot()

    # next available rId: look at all package-namespace Relationship elements
    existing_ids = []
    for rel in rels_root.findall(REL("Relationship")):
        rid = rel.get("Id", "")
        if rid.startswith("rId"):
            try:
                existing_ids.append(int(rid[3:]))
            except ValueError:
                pass
    next_rid = max(existing_ids or [0]) + 1

    def make_hlink_run(text, rid):
        """<w:hyperlink><w:r><w:rPr>(blue+underline)<w:t>text"""
        hlink = etree.Element(f"{{{NS['w']}}}hyperlink")
        hlink.set(f"{{{NS['r']}}}id", rid)

        r = etree.Element(f"{{{NS['w']}}}r")
        r_pr = etree.Element(f"{{{NS['w']}}}rPr")

        u = etree.Element(f"{{{NS['w']}}}u")
        u.set(f"{{{NS['w']}}}val", "single")

        color = etree.Element(f"{{{NS['w']}}}color")
        color.set(f"{{{NS['w']}}}val", "0000FF")

        r_pr.append(u)
        r_pr.append(color)
        r.append(r_pr)

        t = etree.Element(f"{{{NS['w']}}}t")
        set_text_preserve(t, text)
        r.append(t)

        hlink.append(r)
        return hlink

    # ---- for each key, link first occurrence in the document ----
    links_to_insert = len(link_map)
    inserted_link_count = 0
    for key, url in link_map.items():
        if not key:
            continue

        key_linked = False

        for p in root.findall(".//w:p", NS):
            if key_linked:
                break

            runs = p.findall("w:r", NS)
            if not runs:
                continue

            # concatenate text
            full_text = ""
            run_texts = []
            for r in runs:
                t_el = r.find("w:t", NS)
                txt = t_el.text if t_el is not None and t_el.text else ""
                run_texts.append(txt)
                full_text += txt

            if key not in full_text:
                continue

            start = full_text.index(key)
            end = start + len(key)

            # find which runs overlap the key
            cursor = 0
            first_idx = None
            last_idx = None
            for i, txt in enumerate(run_texts):
                length = len(txt)
                r_start = cursor
                r_end = cursor + length
                if r_end > start and r_start < end:
                    if first_idx is None:
                        first_idx = i
                    last_idx = i
                cursor += length

            if first_idx is None:
                continue

            # edit overlapping runs in-place
            cursor = 0
            single_run_after_text = ""

            for i, (r, txt) in enumerate(zip(runs, run_texts)):
                length = len(txt)
                t_el = r.find("w:t", NS)
                r_start = cursor
                r_end = cursor + length

                if t_el is None:
                    cursor += length
                    continue

                if i < first_idx or i > last_idx:
                    cursor += length
                    continue

                overlap_start = max(r_start, start)
                overlap_end = min(r_end, end)
                before_len = max(0, overlap_start - r_start)
                after_len = max(0, r_end - overlap_end)

                before = txt[:before_len]
                after = txt[length - after_len:] if after_len > 0 else ""

                parent = r.getparent()

                if first_idx == last_idx:
                    # key is entirely in this run
                    set_text_preserve(t_el, before)
                    single_run_after_text = after
                else:
                    if i == first_idx:
                        set_text_preserve(t_el, before)
                    elif i == last_idx:
                        set_text_preserve(t_el, after)
                    else:
                        # fully consumed; delete run
                        parent.remove(r)

                cursor += length

            # create Relationship in the CORRECT namespace
            rid = f"rId{next_rid}"
            next_rid += 1

            rel_el = etree.Element(REL("Relationship"))
            rel_el.set("Id", rid)
            rel_el.set("Type", "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink")
            rel_el.set("Target", url)
            rel_el.set("TargetMode", "External")
            rels_root.append(rel_el)

            hlink = make_hlink_run(key, rid)

            # insert hyperlink after the first overlapping run
            p_children = list(p)
            target_run = runs[first_idx]

            if target_run not in p_children:
                p.append(hlink)
            else:
                insert_pos = p_children.index(target_run) + 1
                p.insert(insert_pos, hlink)

                inserted_link_count += 1

                # if single-run case, append "after" text as a cloned run
                if first_idx == last_idx:
                    after_text = single_run_after_text
                    if after_text:
                        after_run = etree.fromstring(etree.tostring(target_run))
                        t_after = after_run.find("w:t", NS)
                        if t_after is None:
                            t_after = etree.SubElement(after_run, f"{{{NS['w']}}}t")
                        set_text_preserve(t_after, after_text)
                        p.insert(insert_pos + 1, after_run)

            key_linked = True  # done with this key

    # write XML back
    tree.write(document_path, xml_declaration=True, encoding="UTF-8", standalone="yes")
    rels_tree.write(rels_path, xml_declaration=True, encoding="UTF-8", standalone="yes")

    # rezip to docx
    shutil.make_archive("output_hlinked", "zip", temp_dir)
    if os.path.exists(output_docx):
        os.remove(output_docx)
    shutil.move("output_hlinked.zip", output_docx)
    shutil.rmtree(temp_dir)

    print(f"\n[OK] Hyperlinked file saved as: {output_docx}\n")

    if links_to_insert != inserted_link_count:
        print(f"***[WARNING]*** Only inserted {inserted_link_count} out of {links_to_insert} links.")

# --------------------------------------------------------------
# MAIN ENTRY POINT
# --------------------------------------------------------------
if __name__ == "__main__":

    """
    Sample command line execution:
    mypackages\insert_links_into_word.py r"C:\my_input.docx" r"C:\my_output.docx" r"C:\my_links_recipe.json"
    """

    """    
    if len(sys.argv) != 4:
        print("Usage: python insert_links_into_word.py <input.docx> <output.docx> <mapping.json>")
        sys.exit(1)
    """

    resume_type = "short"   # "short" is used for the most recent 10 years of work experience only, else for full resume
    input_docx = r"C:\Cagri_Workspace\isbasvuru\My_Resumes\Resume_Cagri_Tanriover_63_OZT.docx"      # sys.argv[1]
    
    ###################################################################
    ###################################################################

    input_filepath = Path(input_docx)
    root = input_filepath.stem  # extracts the root name of the input file

    if resume_type == "short":
        mapping_json = r"C:\Cagri_Workspace\isbasvuru\My_Resumes\resume_hyperlinks_SHORT.json"   # sys.argv[3]
        root = f"{root}_shrt_lnkd"  # derives the output file name using the input file name

    else:
        mapping_json = r"C:\Cagri_Workspace\isbasvuru\My_Resumes\resume_hyperlinks_EXT.json"        # sys.argv[3]
        root = f"{root}_ext_lnkd"  # derives the output file name using the input file name

    output_filepath = input_filepath.with_stem(root)  # Only modifies the file name stem and leaves the extension as is!
    output_docx = str(output_filepath)  # keep the string as is for compatibility with the rest of the code
    add_hyperlinks_to_docx(input_docx, output_docx, mapping_json)

    # 1. Insert hyperlinks
    add_hyperlinks_to_docx(input_docx, output_docx, mapping_json)

    # 2. Compare original vs modified
    compare_docs(input_docx, output_docx, "diff_report.txt")
    print("Comparison complete. See diff_report.txt")