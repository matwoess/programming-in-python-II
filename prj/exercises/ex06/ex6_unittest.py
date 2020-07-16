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

ex_file = 'ex6.py'
full_points = 10
points = full_points
python = sys.executable

with open("unittest_ex6_data.pkl", "rb") as ufh:
    all_inputs_outputs = pkl.load(ufh)

with open(ex_file, 'r') as efh:
    efc = efh.read()
    if efc.find("sklearn") != -1:
        print("Found name of sklearn package in submission file."
              "Please remove the name of the sklearn package,"
              "even if not imported, to receive points.")
        print(f"\nEstimate points upon submission: 0 (also see checklist in moodle).")

feedback = ''

for test_i, (inputs, outputs) in enumerate(all_inputs_outputs):
    
    comment = ''
    fcall = ''
    with open(os.devnull, 'w') as null:
        # sys.stdout = null
        try:
            from prj.exercises.ex06.ex6 import ex6
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
                fcall = f"ex6(logits={inputs[0]}, activation_function={inputs[1]}, threshold={inputs[2]}, targets={inputs[3]}))"
                returns = ex6(logits=inputs[0], activation_function=inputs[1], threshold=inputs[2], targets=inputs[3])
                errs = ''
                if len(returns) != 6:
                    points -= (full_points / len(all_inputs_outputs))
                    comment = f"Output should be: " \
                              f"{outputs} \n" \
                              f"but is {returns}"
                if not all([isinstance(r, float) for r in returns]):
                    points -= (full_points / len(all_inputs_outputs))
                    comment = f"Output should be: " \
                              f"{outputs} \n" \
                              f"but is {returns} " \
                              f"(outputs should be Python float)"
                if not all([r == o for r, o in zip(returns, outputs)]):
                    points -= (full_points / len(all_inputs_outputs))
                    comment = f"Output should be: " \
                              f"{outputs} \n" \
                              f"but is {returns} "
                
            except Exception as e:
                outs = ''
                errs = ''
                if outputs == TypeError or outputs == ValueError:
                    if outputs != type(e):
                        comment = f"Should raise <{outputs}> " \
                                  f"but exception <{type(e)}: {e}> has been raised"
                        points -= (full_points / len(all_inputs_outputs))
                        errs = e
                else:
                    comment = f"Output should be: {outputs} \n" \
                              f"but exception <{type(e)}: {e}> has been raised"
                    points -= (full_points / len(all_inputs_outputs))
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
feedback += f"\nEstimate points upon submission: {points * 1:.2f} (also see checklist in moodle). " \
            f"This is only an estimate, inputs will be different for grading."
print(f"\t{feedback}")
