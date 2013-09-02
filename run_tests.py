import glob
import os
import doctest

import knights_tour_tests_doc as ktdt

pwd = os.getcwd()
for module in glob.glob("*.py"):
    doctest.testfile(module)    


#below could be useful in the future
"""
import fnmatch
import os

matches = []
src = os.getcwd()
for root, dirnames, filenames in os.walk(src):
  for filename in fnmatch.filter(filenames, '*.py'):
      matches.append(os.path.join(root, filename))
"""
