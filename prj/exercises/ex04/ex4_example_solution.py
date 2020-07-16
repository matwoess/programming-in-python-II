# -*- coding: utf-8 -*-
"""
Author -- Michael Widrich
Contact -- widrich@ml.jku.at
Date -- 01.10.2019

###############################################################################

The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.

###############################################################################

Example solution for exercise 4
"""
import numpy as np


def ex4(image_array: np.ndarray, crop_size: tuple, crop_center: tuple):
    """See assignment sheet for usage description"""
    if len(crop_size) != 2 or len(crop_center) != 2:
        raise ValueError(f"crop_size and crop_center must have length 2 but have length {len(crop_size)} "
                         f"and {len(crop_center)}")
    if crop_size[0] % 2 == 0 or crop_size[1] % 2 == 0:
        raise ValueError(f"crop_size must only include odd integer values")
    
    if not isinstance(image_array, np.ndarray) or image_array.ndim != 2:
        raise ValueError(f"image_data must be numpy array of shape (H, W)")
    
    # Compute start and end index of crop for x axis
    crop_x_start = crop_center[0] - int(crop_size[0] / 2)
    crop_x_end = crop_center[0] + int(crop_size[0] / 2)
    # Compute number of border pixels to both sides of crop for x axis
    n_border_pixels_x = [crop_x_start, image_array.shape[0] - 1 - crop_x_end]

    # Compute start and end index of crop for y axis
    crop_y_start = crop_center[1] - int(crop_size[1] / 2)
    crop_y_end = crop_center[1] + int(crop_size[1] / 2)
    # Compute number of border pixels to both sides of crop for y axis
    n_border_pixels_y = [crop_y_start, image_array.shape[1] - 1 - crop_y_end]
    
    if min(n_border_pixels_x) < 20 or min(n_border_pixels_y) < 20:
        raise ValueError(f"border for cropped out rectangle should be >= 20 but is {n_border_pixels_x} "
                         f"and {n_border_pixels_y}")
    
    # We will use slicing -> add 1 to the end indices
    crop_x_end += 1
    crop_y_end += 1
    
    # Make crop_array, mask cropped area with 1, others with 0
    crop_array = np.zeros_like(image_array)
    crop_array[crop_x_start:crop_x_end, crop_y_start:crop_y_end] = 1
    # Make target_array, which is copy of cropped area
    target_array = np.copy(image_array[crop_x_start:crop_x_end, crop_y_start:crop_y_end])
    # Make image_array by setting cropped area to 0
    image_array[crop_x_start:crop_x_end, crop_y_start:crop_y_end] = 0
    
    return image_array, crop_array, target_array
