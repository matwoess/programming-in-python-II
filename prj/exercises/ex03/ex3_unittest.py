"""
Author -- Python Team, Programming in Python II
Contact -- python@ml.jku.at
Date -- 01.03.2020

###############################################################################

The following copyright statement applies to all code within this file.

Copyright statement:
This  material,  no  matter  whether  in  printed  or  electronic  form,
may  be  used  for personal  and non-commercial educational use only.
Any reproduction of this manuscript, no matter whether as a whole or in parts,
no matter whether in printed or in electronic form, requires explicit prior
acceptance of the authors.

###############################################################################

"""

import os
import sys
from glob import glob
import pandas as pd
import numpy as np
import hashlib
import inspect
# time_given = int(15)


ex_file = 'ex3.py'
full_points = 17
points = full_points
python = sys.executable

inputs = sorted(glob(os.path.join("unittest_input_*"), recursive=True))
if not len(inputs):
    raise FileNotFoundError("Could not find unittest_input_* files")

feedback = ''

for test_i, input_folder in enumerate(inputs):
    input_folder = os.path.abspath(input_folder)
    comment = ''
    fcall = ''
    with open(os.devnull, 'w') as null:
        # sys.stdout = null
        try:
            from prj.exercises.ex03.ex3 import ImageNormalizer
            proper_import = True
        except Exception as e:
            outs = ''
            errs = e
            points -= full_points / len(inputs)
            proper_import = False
        finally:
            sys.stdout.flush()
            sys.stdout = sys.__stdout__
    
    if proper_import:
        with open(os.devnull, 'w') as null:
            # sys.stdout = null
            try:
                errs = ''
                input_basename = os.path.basename(input_folder)

                # check constructor
                instance = ImageNormalizer(input_dir=input_folder)
                fcall = f"ImageNormalizer(input_dir={input_folder})"

                # check correct file names + sorting
                tfiles = sorted(glob(os.path.join(f"solutions", input_basename, "*")))
                with open(os.path.join(f"solutions", input_basename, f"filenames.txt"), 'r') as f:
                    filenames_sol = f.read().splitlines()
                    if not (hasattr(instance, 'file_names') and instance.file_names == filenames_sol):
                        points -= full_points / len(inputs) / 3
                        comment += f"File names do not match (see directory 'solutions')\n"

                # check if class has method
                attribute = 'get_stats'
                if not hasattr(instance, attribute):
                    comment += f'  missing attribute {attribute}!\n'
                    points -= full_points / len(inputs) / 3
                else:
                    # check for correct data types
                    stats = instance.get_stats()
                    if not type(stats) is tuple or len(stats) != 2:
                        points -= full_points / len(inputs) / 6
                        comment += f"Incorrect return value of method {attribute}\n"
                    elif stats[0].dtype.num != np.dtype(np.float64).num or stats[1].dtype.num != np.dtype(np.float64).num:
                            points -= full_points / len(inputs) / 6
                            comment += f"Incorrect format of stats arrays\n"
                    # check means and stds
                    else:
                        means = pd.read_csv(os.path.join(f"solutions", input_basename, f"means.csv"), sep=',',
                                            header=None).values.reshape(-1)
                        stds = pd.read_csv(os.path.join(f"solutions", input_basename, f"stds.csv"), sep=',',
                                           header=None).values.reshape(-1)
                        # check if shapes are correct
                        if not means.shape == stats[0].shape or not stds.shape == stats[0].shape:
                            points -= full_points / len(inputs) / 6
                            comment += f"Shapes of stats do not match (see directory 'solutions')\n"
                        elif not np.all(np.isclose(stats[0], means, atol=0)) or not np.all(np.isclose(stats[1], stds, atol=0)):
                            points -= full_points / len(inputs) / 6
                            comment += f"Stats values do not match (see directory 'solutions')\n"

                # load solution images
                image1_sol = pd.read_csv(os.path.join(f"solutions", input_basename, f"image1.csv"), sep=',',
                                         header=None).values
                image2_sol = pd.read_csv(os.path.join(f"solutions", input_basename, f"image2.csv"), sep=',',
                                         header=None).values
                # check if class has method
                attribute = 'get_images'
                if not hasattr(instance, attribute):
                    comment += f'  missing attribute {attribute}!\n'
                    points -= full_points / len(inputs) / 3
                # check for correct data types
                elif not inspect.isgeneratorfunction(instance.get_images):
                    points -= full_points / len(inputs) / 3
                    comment += f"{attribute} is not a generator\n"
                else:
                    img_generator = instance.get_images()
                    image1 = next(img_generator)
                    image2 = next(img_generator)
                    if not type(image1) is np.ndarray:
                        points -= full_points / len(inputs) / 3
                        comment += f"Incorrect format of image (not a numpy array)\n"
                    else:
                        if image1.dtype.num != np.dtype(np.float32).num:
                            points -= full_points / len(inputs) / 12
                            comment += f"Incorrect format of image\n"
                        # check if image values are correct
                        elif not np.all(np.isclose(image1, image1_sol, atol=1e-4)):
                            points -= full_points / len(inputs) / 12
                            comment += f"Normalized image values of first image do not match (see directory 'solutions')\n"
                        elif not np.all(np.isclose(image2, image2_sol, atol=1e-4)):
                            points -= full_points / len(inputs) / 12
                            comment += f"Normalized image values of second image do not match (see directory 'solutions')\n"
                        # check means and std for all images
                        else:
                            for img in instance.get_images():
                                if not np.isclose(np.mean(img), 0, atol=1e-4) or not np.isclose(np.std(img), 1, atol=1e-4):
                                    points -= full_points / len(inputs) / 12 / len(filenames_sol)
                                    comment += f"One or more images are not normalized correctly (see directory 'solutions')\n"
            except Exception as e:
                outs = ''
                errs = e
                points -= full_points / len(inputs)
            finally:
                sys.stdout.flush()
                sys.stdout = sys.__stdout__

    feedback += "#" * 3
    feedback += f" Test {test_i} "
    feedback += "#" * 3
    feedback += f"\nFunctioncall was:\n---\n{fcall}\n---\n"
    feedback += f"Error messages:\n---\n{errs}\n---\n"
    feedback += f"Comments:\n---\n{comment}\n---\n"
    feedback += f"\nCurrent points: {points:.2f} "

points = points if points > 0 else 0
feedback += "#" * 3
print(f"{feedback}\nEstimated points: {points * 1:.4f}")
