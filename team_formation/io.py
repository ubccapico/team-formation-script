import os
import string

from team_formation import config

def get_course_folder_path(course_id):
    course_folder_path = "{}/course_{}".format(get_root_folder(), course_id)
    if not os.path.exists(course_folder_path):
        os.makedirs(course_folder_path)
    return course_folder_path

def get_root_folder():
    folder_path = "{}/{:%Y-%m-%d %H:%M:%S}".format(
        config.DATA_FOLDER,
        config.SCRIPT_CURRENT_TIME
    )
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def get_output_folder():
    folder_path = "{}/output".format(get_root_folder())
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def format_filename(name):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(char for char in name if char in valid_chars)
    filename = filename.replace(' ','_')
    return filename