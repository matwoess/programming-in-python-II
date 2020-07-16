# -*- coding: utf-8 -*-
"""ex2.py
Author: Mathias
Matr.Nr.: k11709064
Exercise 2
"""
import glob
import hashlib
import os
from PIL import Image
import numpy as np
from shutil import copyfile

valid_file_endings = ['jpg', 'JPG', 'jpeg', 'JPEG']
file_size_min = 10_240
min_width_height = 100


def check_rules(file, hashtable):
    filename = os.path.split(file)[-1]
    extension = filename.split('.')[-1]
    if extension not in valid_file_endings:
        return 1
    if os.path.getsize(file) < file_size_min:
        return 2
    try:
        image = Image.open(file)
    except IOError:
        return 3
    image = np.array(image)
    if image.var() == 0:
        return 4
    if len(image.shape) != 2 or image.shape[0] < min_width_height or image.shape[1] < min_width_height:
        return 5
    file_data = image.tobytes()
    hash_fn = hashlib.sha256()
    hash_fn.update(file_data)
    file_hash = hash_fn.digest()
    if file_hash in hashtable:
        return 6
    hashtable.append(file_hash)


def write_errors(error_lines, logfile):
    with open(logfile, 'w') as log:
        log.writelines(error_lines)


def write_files(valid_files, output_dir):
    existing_files = sorted(glob.glob(os.path.join(output_dir, '**/*'), recursive=True))
    for f in existing_files:
        os.remove(f)
    for sid, file in enumerate(valid_files, 1):
        filename = f'{sid:06}.jpg'
        path = os.path.join(output_dir, filename)
        copyfile(file, path)


def ex2(input_dir, output_dir, logfile):
    files = sorted(glob.glob(os.path.join(input_dir, '**/*'), recursive=True))
    files = list(f for f in files if os.path.isfile(f))
    print(f'found {len(files)} files')
    abs_input_dir = os.path.abspath(input_dir) + '/'
    valid_files = list()
    error_lines = list()
    hashtable = list()
    for file in files:
        error_code = check_rules(file, hashtable)
        if error_code:
            relative_name = os.path.abspath(file).replace(abs_input_dir, '')
            error_lines.append(f'{relative_name};{error_code}\n')
        else:
            valid_files.append(file)
        write_files(valid_files, output_dir)
        write_errors(error_lines, logfile)
    return len(valid_files)

# input_dir = './input'
# output_dir = './output'
# logfile = './log.txt'
# successful = ex2(input_dir, output_dir, logfile)
# print(f'valid files: {successful}')
