import os
import sys

# Make the billpad package importable when running pytest from the
# project root, without installing anything.
sys.path.insert(0, os.path.dirname(__file__))
