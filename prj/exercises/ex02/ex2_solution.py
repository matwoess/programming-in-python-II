# -*- coding: utf-8 -*-
"""
ex2 example solution
"""
import os
import shutil
import glob
from PIL import Image
import numpy as np
import hashlib


def ex2(input_dir: str, output_dir: str, logfile: str):
    """See assignment sheet for usage description"""
    # Get sorted list of file names
    input_dir = os.path.abspath(input_dir)
    filenames = glob.glob(os.path.join(input_dir, '**', '*'), recursive=True)
    filenames.sort()
    # Optional: Exclude folder names
    # filenames = [f for f in filenames if os.path.isfile(f)]
    # Optional: Create the output directory if it does not exist
    # os.makedirs(output_dir, exist_ok=True)
    
    # Prepare counter for valid files
    valid_files = 0
    # Prepare list to store image hashes in
    hash_list = []
    # Create clean logfile
    with open(logfile, 'w') as _:
        pass
    # Loop over filenames
    for filename in filenames:
        # Check for rule 1
        if not (filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.JPEG')
                or filename.endswith('.jpeg')):
            # Add line to logfile if rule is violated
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};1", file=lf)
            # Skip to next file if rule was violated
            continue
        # Check for rule 2
        if not os.path.getsize(filename) > 1e4:
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};2", file=lf)
            continue
        # Check for rule 3
        try:
            image = Image.open(filename)
        except:
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};3", file=lf)
            continue
        # Check for rule 4
        np_image = np.array(image)
        if np.std(np_image) <= 0:
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};4", file=lf)
            continue
        # Check for rule 5
        image_shape = np_image.shape
        if not (len(image_shape) == 2 and min(image_shape) >= 100):
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};5", file=lf)
            continue
        # Check for rule 6
        # Get hash value from image data
        np_image_bytes = np_image.tostring()
        hashing_function = hashlib.sha256()
        hashing_function.update(np_image_bytes)
        np_image_hash = hashing_function.digest()
        # Check if image data existed in other file too
        if np_image_hash in hash_list:
            with open(logfile, 'a') as lf:
                print(f"{filename[len(input_dir)+1:]};6", file=lf)
            continue
        # Add image data hash to list of hashes
        hash_list.append(np_image_hash)
        # No rule was violated -> increase counter for new filename and copy file
        valid_files += 1
        shutil.copy(filename, os.path.join(output_dir, f"{valid_files:06d}.jpg"))
    # Return number of valid files
    return valid_files
