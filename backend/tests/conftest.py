import sys
import os
import pytest

# Add the app directory to sys.path for test imports
test_root = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(test_root, '..'))
sys.path.insert(0, project_root)
