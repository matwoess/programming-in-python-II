# -*- coding: utf-8 -*-
"""ex3.py
Author: Mathias
Matr.Nr.: k11709064
Exercise 3
"""
import os
import glob

import numpy as np
from PIL import Image
from tqdm import tqdm


class ImageNormalizer:
    def __init__(self, input_dir=None):
        if input_dir is not None:
            self.base_dir = input_dir
            files = sorted(glob.glob(os.path.join(input_dir, '*.jpg')))
            files = [os.path.split(f)[-1] for f in files if os.path.isfile(f)]
            self.file_names = files

    def get_stats(self):
        means = np.zeros(shape=(len(self.file_names),), dtype=np.float64)
        stds = np.zeros(shape=(len(self.file_names),), dtype=np.float64)
        for i, image_file in tqdm(enumerate(self.file_names),
                                  desc='getting stats', total=len(self.file_names)):
            img = np.array(Image.open(os.path.join(self.base_dir, image_file)))
            means[i] = img.mean()
            stds[i] = img.std()
        return means, stds

    def get_images(self):
        for image in self.file_names:
            img = np.array(Image.open(os.path.join(self.base_dir, image)), dtype=np.float32)
            img /= 255
            img -= img.mean()
            img /= img.std()
            yield img


# input_path = './input'
# normalizer = ImageNormalizer(input_path)
# m, s = normalizer.get_stats()
# means = 0
# for i in normalizer.get_images():
#     means += i.mean()
# print(round(means))
# stds = 0
# for img in normalizer.get_images():
#     stds += img.std()
# stds /= len(normalizer.file_names)
# print(round(stds))
