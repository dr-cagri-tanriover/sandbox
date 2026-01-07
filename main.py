import os
import time
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mypackages import tkint_gui as tkg
from mypackages import pyaudio_tools as aud
from mypackages import activity_sense as acs
from mypackages import face_detector as fd



# Good ref: https://linuxtut.com/en/3c66781f41884694838b/

def fixed_cos_plot():
    x = np.arange(0, 100, 0.1)
    y = np.cos(x)

    fig = plt.figure()
    ax = plt.axes(xlim=(0, 100), ylim=(-1.1, 1.1))
    line = plt.plot(x, y)

    plt.show()

def animated_matplot():
    fig, ax = plt.subplots()

    x = np.arange(0, 2 * np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))

    def animate(i):
        #line.set_ydata(np.sin(x + i / 10.0))  # update the data
        ax.cla()
        ax.plot(x, np.sin(x), color='r')
        ax.plot(x[i], np.sin(x[i]), marker="o", color='b')

    '''
    def animate(i):
        line.set_ydata(np.sin(x + i / 10.0))  # update the data
        return line,
    '''

    # Init only required for blitting to give a clean slate.
    def init():
        line.set_ydata(np.ma.array(x, mask=True))
        return line,

    ani = animation.FuncAnimation(fig, animate, frames=400,
                                  interval=50, blit=False, repeat=False)

    '''
    ani = animation.FuncAnimation(fig, animate, frames=400, init_func=init,
                                  interval=50, blit=False, repeat=False)
    '''

    plt.show()

def file_renamer(fix_unicode_chars=False):

    source_folder='C:\Cagri_Workspace\images_videos\demet_youtube\popular_videos'

    files_path = [os.path.join(source_folder,x) for x in os.listdir(source_folder)]

    for eachFile in files_path:
        # extract the file name with extension first
        path_list = eachFile.split('\\')
        filename_full = path_list[-1]

        # replace each space with = character
        dunder_filename = filename_full.replace(' ', '=')

        # Rejoin all path components EXCEPT the original filename
        partial_path = '\\'.join(path_list[0:len(path_list)-1])

        # Append the space-free filename to the end
        new_filename_full = os.path.join(partial_path, dunder_filename)

        # finally, rename the original filename
        os.rename(eachFile, new_filename_full)

    print(f"Found {len(files_path)}")

    if fix_unicode_chars:
        # Unicode (Turkissh characters will be replaced with 'x'
        print(f"Performing unicode correction...")
        files_path = [os.path.join(source_folder, x) for x in os.listdir(source_folder)]

        for eachFile in files_path:
            # extract the file name with extension first
            path_list = eachFile.split('\\')
            filename_full = path_list[-1]

            bytelist = []
            for eachChar in filename_full:
                # Processing each character of the file name string
                try:
                    bytelist.append(eachChar.encode('ascii'))
                except UnicodeEncodeError:
                    bytelist.append(b'x')  # Unicode error prompts replacement with character 'x' as byte

            # Process the bytelist into a full string
            new_filename = b''.join(bytelist).decode('utf-8')

            # Rejoin all path components EXCEPT the original filename
            partial_path = '\\'.join(path_list[0:len(path_list) - 1])

            # Append the space-free filename to the end
            new_filename_full = os.path.join(partial_path, new_filename)

            # finally, rename the original filename
            os.rename(eachFile, new_filename_full)


def jpeg_renamer():

    source_folder='C:\Cagri_Workspace\images\Demet_Youtube_Thumbnails_jpegs'

    files_path = [os.path.join(source_folder,x) for x in os.listdir(source_folder)]

    for eachFile in files_path:
        # extract the file name with extension first
        path_list = eachFile.split('\\')
        filename_full = path_list[-1]

        # replace each = with " " characters
        space_filename = filename_full.replace('=', ' ')

        # get file base name and its extension
        base_name, extension = os.path.splitext(space_filename)

        # add 2022 to base name
        base_name += ' 2022'

        # Reconstruct full file name
        space_filename = base_name + extension

        # Rejoin all path components EXCEPT the original filename
        partial_path = '\\'.join(path_list[0:len(path_list)-1])

        # Append the space-free filename to the end
        new_filename_full = os.path.join(partial_path, space_filename)

        # finally, rename the original filename
        os.rename(eachFile, new_filename_full)

    print(f"Found {len(files_path)}")


def convert_webp_to_jpg():

    source_folder='C:\Cagri_Workspace\images\Demet_Youtube_Thumbnails_working'
    ffmpeg_command ='C:\\Cagri_Workspace\\utilities\\ffmpeg\\ffmpeg-4.4.1-full_build\\bin\\ffmpeg.exe'

    files_path = [os.path.join(source_folder, x) for x in os.listdir(source_folder)]

    for eachFile in files_path:
        path_list = eachFile.split('\\')
        filename_full = path_list[-1]

        root_filename = filename_full.split('.')[0]
        if filename_full.split('.')[-1] == 'webp':
            # target extension OK
            target_path = '\\'.join(path_list[0:len(path_list)-1])
            target_filename = root_filename + '.jpg'
            target_path = os.path.join(target_path, target_filename)

            command_args = " -i" + " " + eachFile + " " + target_path
            command_string = ffmpeg_command + command_args
            subprocess.run(command_string)
            time.sleep(1)

def text_file_line_processor():

    in_filepath = r"C:\Cagri_Workspace\circuitapps\admin\amazon_review_links.txt"
    out_filepath = r"C:\Cagri_Workspace\circuitapps\admin\amazon_review_links_CLEAN.txt"

    # Read each line into a list
    with open(in_filepath, 'r') as file:
        lines = file.readlines()

    print(f"Found {len(lines)} entries")

    clean_list = []
    for each_line in lines:
        if len(each_line) > 0:
            _stripped = each_line.strip()  # no trailing or leading whitespace characters
            if len(_stripped):
                clean_list.append(_stripped.split('?')[0])  # only keep the first part BEFORE the question mark

    print(f"There are {len(clean_list)} clean entries")

    # Write the list of strings to a text file
    with open(out_filepath, 'w') as file:
        for line in clean_list:
            file.write(line + '\n')

if __name__ == '__main__':
    text_file_line_processor()
    #animated_matplot()
    #tkg.basic_gui()
    #aud.audio_recorder()
    #tkg.p101_application()
    #------- Demet Youtube thumbnail conversion and 2022 renaming steps follow ---------
    #file_renamer(fix_unicode_chars=True) # Step 1
    #convert_webp_to_jpg()  # Step 2
    #jpeg_renamer()  # Step 3
    #----- Computer keyboard and mouse activity sensing script -------
    #acs.monitor_activity()
    # Face detection application
    #fd.detect_face()  # Step 1 - Detect faces and identify bounding box values for each face to generate json records.
    #fd.crop_faces()  # Step 2 - Extracts face parts from each still image and saves them as new images

    # Info on inserting transparent video on image using ffmpeg:
    # https://askandroidquestions.com/2021/05/28/overlay-a-transparent-video-on-image-and-export-into-gif-using-ffmpeg-in-android/
    # Search for transparency setting on videos and overlaying onto static images.