# -*- coding: utf-8 -*-
"""
ex3 example solution
"""
import os
import glob
from PIL import Image
import numpy as np


class ImageNormalizer(object):
    def __init__(self, input_dir: str):
        """See Assignment 1, exercise 3 for description
        
        We have 2 basic options:
        1.: Read all files at once, perform computations and store results in
            RAM (e.g. as attributes).
            This would result in higher performance (we only need to read files
            and calculate mean, std, and normalization once) but would consume
            more RAM. Alternatively, we could pre-compute the results once and
            store them on the hard drive using temporary files.
        2.: Read files and perform computations on-the-fly every time
            get_stats() and get_images() is called. This requires more read and
            computation operations but will require less RAM.
        Since our dataset could be very large, this implementation uses
        option 2.
        """
        # Get sorted list of file names
        file_paths = sorted(glob.glob(os.path.join(input_dir, '*.jpg')))
        # Store file names in attribute (could be used as sample IDs later)
        self.file_names = [os.path.basename(x) for x in file_paths]
        # We will need the path for reading the files in the other methods
        self.input_dir = input_dir
    
    def get_stats(self):
        # Prepare empty arrays for storing means and stds
        means = np.empty(shape=(len(self.file_names),), dtype=np.float64)
        stds = np.empty(shape=(len(self.file_names),), dtype=np.float64)
        # Loop through file names
        for i, filename in enumerate(self.file_names):
            # Open file with file name in self.input_dir
            with Image.open(os.path.join(self.input_dir, filename)) as image:
                # Read image as numpy array
                np_image = np.array(image)
            # Compute and store mean and std
            means[i] = np.mean(np_image)
            stds[i] = np.std(np_image)
        return means, stds
    
    def get_images(self):
        # Loop through file names, 1 file at a time (less RAM consumption)
        for filename in self.file_names:
            # Open file with file name in self.input_dir
            with Image.open(os.path.join(self.input_dir, filename)) as image:
                # Read image as numpy array with np.float32 datatype
                np_image = np.array(image, dtype=np.float32)
            # Normalize image to mean=0 and std=1 (-> variance=1)
            np_image_normalized = (np_image - np_image.mean()) / np_image.std()
            # Yield 1 normalized array at a time as generator (also see
            # 03_functions_print_input_modules.py of Programming in Python I)
            yield np_image_normalized
