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
from glob import glob
import pickle
import numpy as np
import signal
import hashlib
time_given = int(15)

def handler(signum, frame):
    raise TimeoutError(f"Timeout after {time_given}sec")

signal.signal(signal.SIGALRM, handler)

ex_file = 'ex2.py'
full_points = 17
points = full_points
python = sys.executable

inputs = sorted(glob(os.path.join("unittest_input_*"), recursive=True))
if not len(inputs):
    raise FileNotFoundError("Could not find unittest_input_* files")

feedback = ''
with open(os.path.join('solutions', 'counts_hashes.csv'), 'r') as fh:
    counts_hashes = fh.read().split('\n')

for test_i, input_folder in enumerate(inputs):
    input_folder = os.path.abspath(input_folder)
    comment = ''
    fcall = ''
    with open(os.devnull, 'w') as null:
        # sys.stdout = null
        try:
            signal.alarm(time_given)
            from prj.exercises.ex02.ex2 import ex2
            signal.alarm(0)
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
                signal.alarm(time_given)
                input_basename = os.path.basename(input_folder)
                output_dir = os.path.join(f"outputs", input_basename)
                logfilepath = output_dir + ".log"
                counts = ex2(input_dir=input_folder, output_dir=output_dir, logfile=logfilepath)
                fcall = f"ex2(input_dir={input_folder}, output_dir={output_dir}, logfile={logfilepath})"
                signal.alarm(0)
                errs = ''
                
                files = sorted(glob(os.path.join(f"outputs", input_basename, "**", "*"), recursive=True))
                tfiles = sorted(glob(os.path.join(f"solutions", input_basename, "**", "*"), recursive=True))
                with open(os.path.join(f"outputs", f"{input_basename}.log"), 'r') as lfh:
                    logfile = lfh.read()
                with open(os.path.join(f"solutions", f"{input_basename}.log"), 'r') as lfh:
                    tlogfile = lfh.read()
                with open(os.path.join(f"solutions", f"{input_basename}_nodirs.log"), 'r') as lfh:
                    tlogfile_nodirs = lfh.read()
                hashing_function = hashlib.sha256()
                for file in files:
                    with open(file, 'rb') as fh:
                        hashing_function.update(fh.read())
                hash = hashing_function.digest()
                tcounts, thashes = counts_hashes[test_i].split(';')
                if not counts == int(tcounts):
                    points -= full_points / len(inputs)
                    comment = f"Function should return {tcounts} but returned {counts}"
                elif not hash == eval(thashes):
                    points -= full_points / len(inputs)
                    comment = f"Contents of output directory do not match (see directory 'solutions')"
                elif not [f.split(os.path.sep)[-2:] for f in files] == [f.split(os.path.sep)[-2:] for f in tfiles]:
                    points -= full_points / len(inputs)
                    comment = f"Contents of output directory do not match (see directory 'solutions')"
                elif not (logfile == tlogfile or logfile == tlogfile_nodirs):
                    points -= full_points / len(inputs)
                    comment = f"Contents of logfiles do not match (see directory 'solutions')"
                
            except Exception as e:
                outs = ''
                errs = e
                points -= full_points / len(inputs)
            finally:
                sys.stdout.flush()
                sys.stdout = sys.__stdout__
    
    feedback += "#" * 3
    feedback += f"Test {test_i}"
    feedback += "#" * 3
    feedback += f"Functioncall was:\n---\n{fcall}\n---\n"
    feedback += f"Error messages:\n---\n{errs}\n---\n"
    feedback += f"Comments:\n---\n{comment}\n---\n"
    feedback += f"Current points:{points:.2f}"

points = points if points > 0 else 0
feedback += "#" * 3
feedback += "\nPlease remove folder 'outputs' manually or use it to check your output vs. the solutions in 'solutions'"
print(f"{points * 1:.4f}\t{feedback}")
