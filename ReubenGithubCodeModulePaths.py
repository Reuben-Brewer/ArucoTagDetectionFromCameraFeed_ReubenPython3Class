import sys
from pathlib import Path

GDRIVE_ROOT = Path(r"G:\My Drive\CodeReuben")

def Enable():
    PathToAdd = str(GDRIVE_ROOT)
    if PathToAdd not in sys.path:
        sys.path.insert(0, PathToAdd)