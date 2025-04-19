REM  This Windows batch file runs the ARISS Clock using Python.
REM  Python must be installed for this to work.
REM
REM  In Windows, make a shortcut to this batch file.
REM  Set the icon to the icon fine in the ARISS_Clock_V3.0.0 folder.
REM  Suggest selecting "Minimize Window" option to not show the 
REM  Command Line window. Note that it will open Notepad under
REM  any windows already open.
REM
REM  Once a shortcut has been created, it can be copied to the 
REM  desktop.
REM
REM  ARISS Clock - Version 3.0.0
REM    Usage: ARISS_Clock [ -b ] [ -c ] [ -e ] [ -h ] [ -l ] [ -t ]
REM  COMMAND LINE OPTIONS
REM    -b, -B, --BW      Rise/Set timers only in black and white.
REM    -c, -C, --Color   Do NOT show background colors.
REM    -e, -E, --Event   Do NOT show the event local time clock.
REM    -h, -H, --Help    Lists the command line options, then exits.
REM    -l, -L, --Labels  Do NOT show the display of timer and clock labels.
REM    -t, -T, --Top     Force clocks to the top of the timer display.
REM  If any option is invalid, the program ignores them all.
REM  See ARISS_Clock_readme.txt for more details.
REM
REM  Uncomment the one you want to use, or create new ones.

REM  Default. No features turned off.
python ARISS_Clock.py

REM  Turn off local event time clock. 
REM  Use this if the clock is being use locally at the event.
REM python ARISS_Clock.py -e

REM  Turn off labels. A bit more compact.
REM python ARISS_Clock.py -l
