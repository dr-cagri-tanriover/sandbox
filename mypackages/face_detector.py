import cv2
import os
import copy
import json
import subprocess

def detect_face():
    src_folder = 'C:\Cagri_Workspace\images_videos\demet_youtube\hand_mov_stills'
    dest_folder = 'C:\Cagri_Workspace\images_videos\demet_youtube\hand_mov_faces'
    file_attrib = {'stem': 'hand_', 'ext': '.jpg'}
    start_frame_no = 1
    end_frame_no = 6038

    # Load the cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    face_record_template = {'filename': '', 'x': '0', 'y': '0', 'width': '0', 'height': '0'}
    face_records_dict = {}  # will include multiple records of face_record_template
    for idx in range(start_frame_no - 1, end_frame_no):
        #idx starts at 0
        file_index_str = str(idx + 1).rjust(6, '0')  # pad zeros on the left to have 6 digits
        current_filename = file_attrib['stem'] + file_index_str + file_attrib['ext']
        full_file_path = os.path.join(src_folder, current_filename)
        # Read the input image
        img = cv2.imread(full_file_path)

        # Convert into grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 4, minSize=[300, 300])

        # Identify the largest face found
        max_width = 0
        #face_dim = (0, 0, 0, 0)
        x_cor, y_cor, width, height = 0, 0, 0, 0
        for (x, y, w, h) in faces:
            if w > max_width:
                x_cor, y_cor, width, height = (x, y, w, h)
            #else use the previous frame values

        # Assign to face records
        face_record_template['filename'] = current_filename
        face_record_template['x'] = str(x_cor)
        face_record_template['y'] = str(y_cor)
        face_record_template['width'] = str(width)
        face_record_template['height'] = str(height)

        # Then assign the record to main dictionary under file name key
        face_records_dict[idx] = copy.deepcopy(face_record_template)

        #cv2.rectangle(img, (x_cor, y_cor), (x_cor + width, y_cor + height), (255, 255, 0), 4)
        #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        #full_file_path = os.path.join(dest_folder, current_filename)
        #cv2.imwrite(full_file_path, img)
        print(f" Processed image {idx + 1} of {end_frame_no}")
        # Display the output
        #cv2.imshow('image', img)
        #cv2.waitKey()

    # Write face_records_dict to file to complete
    full_file_path = os.path.join(src_folder, "hand_face_records.json")
    with open(full_file_path, 'w') as fp:
        json.dump(face_records_dict, fp)


def crop_faces():
    face_record_file = 'hand_face_records.json'
    src_folder = 'C:\Cagri_Workspace\images_videos\demet_youtube\hand_mov_stills'
    file_attrib = {'stem': 'facesOfhand_', 'ext': '.jpg'}

    # Read face record json as dictionary
    # Important: each field in JSON file will be read as a string (including numbers ! )
    full_file_path = os.path.join(src_folder, face_record_file)
    with open(full_file_path, 'r') as fp:
        face_records = json.load(fp)

    num_records = len(face_records)  # each record is also a still image file
    print(f"Found {num_records} records in json file")

    # Format of each record is:
    #  { <string idx> : {'filename': '', 'x': '0', 'y': '0', 'width': '0', 'height': '0'}, ... }

    for eachItem in face_records:
        current_image_file = face_records[eachItem]['filename']  # get filename
        file_index_string = current_image_file.split('.')[0].split('_')[-1]  # gets the file number as string
        dest_image_file = file_attrib['stem'] + file_index_string + file_attrib['ext']  # face image file to save
        full_input_path = os.path.join(src_folder, current_image_file)
        full_output_path = os.path.join(src_folder, dest_image_file)
        x_cor = int(face_records[eachItem]['x'])  # x coordinate of detected face
        y_cor = int(face_records[eachItem]['y'])  # y coordinate of detected face
        width = int(face_records[eachItem]['width'])  # width of detected face
        height = int(face_records[eachItem]['height'])  # height of detected face

        if width == 0 or height == 0:
            width, height = 10, 10  # hardcode a default value for 0 sized detections.

        # Create a call to ffmpeg for the cropping operation next
        command_string = "ffmpeg -i " + full_input_path + ' '
        command_string += '-vf ' + '\"crop=' + str(width) + ':' + str(height) + ':' + str(x_cor) + ':' + str(y_cor) + '\" '
        command_string += full_output_path

        subprocess.run(command_string)

        # crop command: ffmpeg -i input.jpg -vf "crop=w:h:x:y" input_crop.jpg
        # where -vf  video filter w : width , h height , x and y are the left top coordinates of image

