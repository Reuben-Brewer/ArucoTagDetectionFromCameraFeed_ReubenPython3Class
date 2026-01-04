# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision H, 01/02/2026

Verified working on: Python 3.12/13 for Windows 10/11 64-bit (Backend = "CAP_DSHOW") and Raspberry Pi Bullseye (Backend = "CAP_ANY").
'''

#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
__author__ = 'reuben.brewer'
__version__ = "Software Revision H, 01/02/2026"

from .ArucoTagDetectionFromCameraFeed_ReubenPython3Class import ArucoTagDetectionFromCameraFeed_ReubenPython3Class

'''
I need the __init__.py file because the directory has the same name as the Python file that it contains.

from ._ReubenPython3Class

The leading . means “from the same package as this file”. This is called a relative import.
Python looks for: current_package/_ReubenPython3Class.py
This only works inside a package (i.e. inside a directory that has __init__.py).

import GetCPUandMemoryUsageOfProcessByPID_ReubenPython3Class

This imports the class with that exact name (not the module, not the package, just the class object itself)
After this line runs, the class is available in the current namespace.
What the whole line does together: It re-exports the class from the inner .py file at the package level.
'''
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################