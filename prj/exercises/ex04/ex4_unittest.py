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

"""

import os
import sys
import dill as pkl
import numpy as np

ex_file = 'ex4.py'
full_points = 15
points = full_points
python = sys.executable

with open("unittest_inputs_outputs_4.pkl", "rb") as ufh:
    all_inputs_outputs = pkl.load(ufh)
    all_inputs = all_inputs_outputs['inputs']
    all_outputs = all_inputs_outputs['outputs']

feedback = ''

for test_i, (inputs, outputs) in enumerate(zip(all_inputs, all_outputs)):
    
    comment = ''
    fcall = ''
    with open(os.devnull, 'w') as null:
        # sys.stdout = null
        try:
            from prj.exercises.ex04.ex4 import ex4
            proper_import = True
        except Exception as e:
            outs = ''
            errs = e
            points -= (full_points / len(all_inputs_outputs) + 4 * (test_i < 3))
            proper_import = False
        finally:
            sys.stdout.flush()
            sys.stdout = sys.__stdout__
    
    if proper_import:
        with open(os.devnull, 'w') as null:
            # sys.stdout = null
            try:
                fcall = f"ex4(image_array={inputs[0]}, crop_size={inputs[1]}, crop_center={inputs[2]}))"
                returns = ex4(image_array=inputs[0], crop_size=inputs[1],
                              crop_center=inputs[2])
                errs = ''
                if (len(returns) != 3
                        or not isinstance(returns[0], np.ndarray)
                        or returns[0].dtype != outputs[0].dtype
                        or returns[0].shape != outputs[0].shape
                        or np.any(returns[0] != outputs[0])):
                    points -= (full_points / len(all_inputs) + 4 * (test_i < 3)) / 3
                    comment = f"Output should be: " \
                              f"({outputs} \n" \
                              f"but is {returns}"
                if (len(returns) != 3
                        or not isinstance(returns[1], np.ndarray)
                        or returns[1].dtype != outputs[1].dtype
                        or returns[1].shape != outputs[1].shape
                        or np.any(returns[1] != outputs[1])):
                    points -= (full_points / len(all_inputs) + 4 * (test_i < 3)) / 3
                    comment = f"Output should be: " \
                              f"({outputs} \n" \
                              f"but is {returns}"
                if (len(returns) != 3
                        or not isinstance(returns[2], np.ndarray)
                        or returns[2].dtype != outputs[2].dtype
                        or returns[2].shape != outputs[2].shape
                        or np.any(returns[2] != outputs[2])):
                    points -= (full_points / len(all_inputs) + 4 * (test_i < 3)) / 3
                    comment = f"Output should be: " \
                              f"({outputs} \n" \
                              f"but is {returns}"
                
            except Exception as e:
                outs = ''
                errs = ''
                if isinstance(outputs, str):
                    if not isinstance(e, ValueError):
                        comment = f"{outputs} " \
                                  f"but exception <{type(e)}: {e}> has been raised"
                        points -= (full_points / len(all_inputs) + 4 * (test_i < 3))
                        errs = e
                else:
                    comment = f"Output should be: {outputs} \n" \
                              f"but exception <{type(e)}: {e}> has been raised"
                    points -= (full_points / len(all_inputs) + 4 * (test_i < 3))
                    errs = e
            finally:
                sys.stdout.flush()
                sys.stdout = sys.__stdout__
    points = max(0, points)
    feedback += "#" * 3
    feedback += f"Test {test_i}"
    feedback += "#" * 3
    feedback += f"\nFunctioncall was:\n---\n{fcall}\n---\n"
    feedback += f"Error messages:\n---\n{errs}\n---\n"
    feedback += f"Comments:\n---\n{comment}\n---\n"
    feedback += f"Current points:{points:.2f}\n"

points = points if points > 0 else 0
feedback += "#" * 3
feedback += f"\nEstimate points upon submission: {points * 1:.2f} (also see checklist in moodle)."
print(f"\t{feedback}")
