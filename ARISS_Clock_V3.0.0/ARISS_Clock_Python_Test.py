"""
| NAME: ARISS Clock Python Test
| BY: Ken McCaughey (N3FZX)
| ON: 2025-03-14
| PROJECT: ARISS Clock
| SCRIPT: ARISS_Clock_Python_Test.py
| VERSION: 1.0.0
| STATUS: Final version.
| SPDX-FileCopyrightText: 2025 Ken McCaughey
| SPDX-License-Identifier: Creative Commons Attribution-ShareAlike 4.0

PURPOSE:
  Test script for new Python users.
  
  Also helps to verify Python libraries for ARISS Clock was loaded
  properly using pip or other means.

USAGE:
  Using terminal window, change to the folder where this script resides.
  Use "cd" command to change directories. Use "ls" or "dir" to list files
  and verify this file is present.
  
  At command line run this script:
  
      python3 ARISS_Clock_Python_Test.py
  
  Will get errors if needed libraries are not installed.
  Use "pip" command to install any missing libraries.
"""

# === LIBRARIES (must be first) ===
import sys
import os
import platform
import getopt
import tkinter as tk
import tkinter.font as tkFont
import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta


# Version info
version_date = '2025-03-14'
version = '1.0.0'

# ========================================================================
# MAIN
# ========================================================================

# Print welcome message.
print()
print('Python script: ARISS_Clock_Python_Test.py')
print('    V.:', version)
print('    By: Ken McCaughey, N3FZX')
print('    On:', version_date)
print()
print('Hello World!')
currentDateAndTime = datetime.now()  # Get date/time from computer.
print("The current date and time is", currentDateAndTime)
print()
print('This is a simple test script for new Python users.')
print('It is intended to make sure scripts can be executed.')
print('This checks for Python libraries needed by ARISS Clock.')
print()
print('The libraries needed by ARISS Clock are present.')
print()
print('Success! Congratulations, you just ran a Python script.')
print()
print('Don\'t forget to install the two needed fonts.')
print()

# End of script
