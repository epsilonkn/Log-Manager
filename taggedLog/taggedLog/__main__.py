import sys
from importlib.metadata import version

if "--version" in sys.argv:
    print("taggedLog", version("taggedLog"))