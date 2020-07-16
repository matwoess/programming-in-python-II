# -*- coding: utf-8 -*-
"""ex4.py
Author: Mathias
Matr.Nr.: k11709064
Exercise 4
"""
import numpy as np


def ex4(image_array: np.ndarray, crop_size: tuple, crop_center: tuple) -> tuple:
    # check parameters
    if not isinstance(image_array, np.ndarray) or len(image_array.shape) != 2:
        raise ValueError('image_array is not a 2D numpy array')
    elif len(crop_size) != 2 or len(crop_center) != 2:
        raise ValueError('crop size or crop center tuples have invalid amount of values')
    elif crop_size[0] % 2 == 0 or crop_size[1] % 2 == 0:
        raise ValueError('crop size contains an even number')
    # check rectangle position
    crop_margin = 20
    min_x = crop_center[0] - crop_size[0] // 2
    max_x = crop_center[0] + crop_size[0] // 2
    min_y = crop_center[1] - crop_size[1] // 2
    max_y = crop_center[1] + crop_size[1] // 2
    if not (crop_margin <= min_x and max_x < image_array.shape[0] - crop_margin and
            crop_margin <= min_y and max_y < image_array.shape[1] - crop_margin):
        raise ValueError('the crop rectangle is too close to the edges')
    # create crop array
    crop_array = np.zeros_like(image_array)
    crop_array[min_x:max_x + 1, min_y:max_y + 1] = 1
    # target_array = crop region in image_array
    target_array = np.copy(image_array[min_x:max_x + 1, min_y:max_y + 1])
    # set image_array values in crop region to 0 (in-place)
    image_array[min_x:max_x + 1, min_y:max_y + 1] = 0
    return image_array, crop_array, target_array

# if __name__ == '__main__':
#     import glob
#     import os
#     import matplotlib.pyplot as plt
#     from PIL import Image
#
#     input_dir = 'input'
#     files = sorted(glob.glob(os.path.join(input_dir, '*.jpg')))
#     for file in files:
#         im_array = np.copy(np.asarray(Image.open(file)))
#         i, c, t = ex4(
#             im_array,
#             (251, 501),
#             (int(im_array.shape[1] / 2), int(im_array.shape[0] / 2 - 200))
#         )
#         plt.imshow(i)
#         plt.show()
#         plt.imshow(c)
#         plt.show()
#         plt.imshow(t)
#         plt.show()
