# === ARISS_Clock.py =====================================================
"""
| NAME: ARISS Clock
| BY: Ken McCaughey (N3FZX)
| ON: 2024-12-12
| VERSION: Dev14
| STATUS: Final development version for V2.0.0.
| SPDX-FileCopyrightText: 2024 Ken McCaughey
| SPDX-License-Identifier: Creative Commons Attribution-ShareAlike 4.0

PURPOSE:
  Provide a simple, readable, large clocks and timers to support ISS
  passes in support of ARISS school contacts at ground station K6DUE.
  Used to help keep track of the countdown to AOS.

DISCLAIMER:
  This free software is provided as is.

DESCRIPTION:
  - Shows ground station local, UTC, and optionally the local school times.
    Reads school time zone UTC offset, ISS Rise and Set times from a config
    file. Shows a countdown to Rise and Set. Once Rise is zero, the pass
    elapsed time timer starts. This timer stops at Set, showing the total
    elapsed time of the pass.
  - Uses local time for Rise and Set. UTC and school times are for
    informational purposes only. All Rise/Set events are triggered
    based on local time clock.
  - If Rise and Set are more that 24 hours out, the time will roll
    over and the ET will not trigger. The date matters!
  - The window fonts can be resized by changing the width. Height can be
    changed as well, but it does not affect the font scaling. Can change
    height to rollup clock or timers from the bottom to hide them.
  - There is a button to view the predicted Rise/Set date/times.
  - There is limited error checking included. Error message window reports
    missing or incorrect Rise/Set time, or if Rise is after Set. A
    default Rise/Set is substituted.

USAGE:
  - Made to work under Python 3.x using Tkinter.
  - Not all systems may have the fonts used. Readme has info on
    where to get the fonts used.
  - Requires ARISS_logo.png file to be present.
  - Requires ARISS_logo_simple.ico to be present for MS-Win.
  - Command line options for help, clock & timer positions, colors,
    and showing the school local time. See readme text.
  - Automatically creates a readme file modeled after a man page.
  - If config file does not exist, one will be created. A message
    window will provide instructions.
  - Edit config file first with new school local time zone UTC offset,
    Rise and Set date/times. Start program. Config file needs to be in
    same folder as executable.
  - Checks for missing or incorrect Rise and Set from the config file.
    Opens a message window and uses default Rise/Set date/times.
  - Checks that Rise is before Set. If not it opens a message window.
  - There are a button to view the Rise/Set predicts.

MAKING AN EXECUTABLE
  - Can be made into an executable using pyinstaller.
  - Will require files ARISS_logo_simple.png and ARISS_logo_simple.ico.
  - On Linux use command line:
      pyinstaller --onefile -w -F -i "ARISS_logo_simple.ico" --add-data 'ARISS_logo.png:.' ARISS_Clock.py
  - Windows 10 pyinstaller command line
      pyinstaller -w -F -i "ARISS_logo_simple.ico" --add-data ARISS_logo.png;. --add-data ARISS_logo_simple.ico;. ARISS_Clock.py

EXTERNAL CREDITS:
  - CREATE A GUI DIGITAL CLOCK USING TIME AND TKINTER LIBRARIES.
  - https://cppsecrets.com/users/218111411511410110199104971141051161049764103109971051084699111109/Python-GUI-Digital-Clock.php

TODO (Top Level):
 - Requires logo file to be present. Consider error checking if logo is missing.
 - Possibly rework timer calculations to be all based on UTC clock.
 - Not sure if daylight savings time is handled correctly. Don't have a good way
   to test.
 - Test again when daylight savings time resumes to check for one hour offesets.  
"""

# === LIBRARIES (must be first) ==========================================
import sys
import os
import platform
import getopt
import tkinter as tk
import time
from datetime import datetime
from datetime import timezone
from datetime import timedelta
import re

# === CONFIGURATION ======================================================
# This section contains some parameters to tweak the look and feel.
# Colors and window geometry are found further below.

Ver = '2.0.0'  # Version of this script.
Rel_date = '2024-12-12'

# Command line option defaults.
#   If these are changed, update def startup() and the readme text in def make_readme_file().
timer_color = False            # -b option. Timer in black & white. Default = False. In color.
background_color = True        # -c option. Default = False. No color.
display_labels = True          # -l option. Show timer/clock labels. Default = False. Do not show.
show_school_clock = True       # -s option. Default = False. Do not show school clock.
display_rise_set_et_top = True  # -t option. Show Rise/Set and ET clocks on top. Default = True. On top.

# When to change colors on timers in seconds before Rise.
yellow_alert = 360  # Nominally 360 sec, = 6 min.
red_alert = 60  # Nominally 60 sec, = 1 min.

# Text baseline characteristics.
text_font = 'DejaVu Sans Mono'  # May not exist on all systems. See readme notes.
text_large = 40  # Used for clocks.
text_med = 25  # Used for window title.
text_small = 15  # Used for most all other text.
text_smaller = 10  # Used for some text.

# --- Declare variables --------------------------------------------------
# Config file should be in same folder as executable. Do NOT change these.
file_config = 'ARISS_Clock_config.txt'
file_readme = 'ARISS_Clock_readme.txt'
a_dictionary = {'STZ': '0', 'RS': '', 'ST': ''}  # Dictionary default keys.


# ========================================================================
# FUNCTIONS
# ========================================================================

def print_help():
    """
    Description:
      - List the command line options and exit.
      - Initiated with the -h, -H, --Help command line option.
      - Exits the program.

    TODO (Help): None.
    """
    # Help message interior double quotes prevent the OS echo cmd from removing extra white spaces.
    help_message = ['"ARISS Clock - Version "' + Ver,
                    '"  Usage: ARISS_Clock [ -b ] [ -c ] [ -h ] [ -l ] [ -s ] [ -t ]"',
                    '"COMMAND LINE OPTIONS"',
                    '"  -b, -B, --BW      Rise/Set timers only in black and white."',
                    '"  -c, -C, --Color   Do NOT show background colors."',
                    '"  -h, -H, --Help    Lists the command line options, then exits."',
                    '"  -l, -L, --Labels  Do NOT show the display of timer and clock labels."',
                    '"  -s, -S, --School  Do NOT show the school local time clock."',
                    '"  -t, -T, --Top     Force clocks to the top of the display."',
                    '"If any option is invalid, the program ignores them all."',
                    '"See ARISS_Clock_readme.txt for more details."']
    i = 0
    while i < len(help_message):
        os.system('echo ' + help_message[i])
        i = i + 1
    sys.exit(0)  # Exit the script.


def startup():
    """
    Description:
      - Reads and parses command line arguments.
      - Sets option flags.
      - On error, use defaults.
      - Requires import of sys, getopt

    TODO (Startup): None.

    External Credits:
      Command Line Arguments in Python
      https://www.geeksforgeeks.org/command-line-arguments-in-python/
    """
    # Remove 1st argument from the list of command line arguments
    global display_labels
    global display_rise_set_et_top
    global timer_color
    global background_color
    global show_school_clock
    argument_list = sys.argv[1:]
    # print(argument_list)
    # Command line options.
    options = 'bBcChHlLsStT'
    # Long options
    long_options = ['BW', 'BW',
                    'Color', 'Color',
                    'Help', 'Help',
                    'Labels', 'Labels',
                    'School', 'School'
                    'Top', 'Top', ]
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argument_list, options, long_options)
        # checking each argument
        for currentArgument, currentValue in arguments:
            if currentArgument in ('-b', '-B', '--BW'):
                timer_color = True
            elif currentArgument in ('-c', '-C', '--Color'):
                background_color = False
            elif currentArgument in ('-h', '-H', '--Help'):
                print_help()
            elif currentArgument in ('-l', '-L', '--Labels'):
                display_labels = False
            elif currentArgument in ('-s', '-S', '--School'):
                show_school_clock = False
            elif currentArgument in ('-t', '-T', '--Top'):
                display_rise_set_et_top = False
    except getopt.error:
        timer_color = False             # -b option, default = False.
        background_color = True         # -c option, default = True.
        display_labels = True           # -l option, default = True.
        show_school_clock = True        # -s option, default = True
        display_rise_set_et_top = True   # -t option, default = True.
    # Uncomment to use for debugging.
    # except getopt.error as err:
    #     output error, and return with an error code
    #     print('Error:', str(err))
    #     display_predicts = False  # Rise/Set predicts shown in main display?


def set_window_height():
    """
    Description:
      - Get the window height based on command line options that affect height.
      - Baseline window geometries are defined here.

    TODO (Set Window Height): None.
    
    :returns:
      window_size_calc (str): Width x height
      window_width_baseline (int): default window width
    """
    # Set geometry based on whether Rise/Set is on main display, as set in config above.
    # Window baseline geometry characteristics.
    window_width_baseline = 500  # Default for all variations.
    window_height1 = 810  # With school clock and labels. Options -l, -s.
    window_height2 = 700  # With labels and without school clock. Option -l.
    window_height3 = 630  # With school clock. Option -s.
    window_height4 = 530  # Without timer/clock labels or school clock. Default.
    if display_labels & show_school_clock:
        window_size_calc = str(window_width_baseline) + 'x' + str(window_height1)
    elif display_labels:
        window_size_calc = str(window_width_baseline) + 'x' + str(window_height2)
    elif show_school_clock:
        window_size_calc = str(window_width_baseline) + 'x' + str(window_height3)
    else:  # Without labels or school clock. Default.
        window_size_calc = str(window_width_baseline) + 'x' + str(window_height4)
    # print('Window size:', window_size_calc)
    return window_size_calc, window_width_baseline


def resource_path(relative_path):
    """
    Description:
      Find relative path to logo files.

    TODO (Resource Path): Fix exception.

    :param relative_path: str
    :return: os.path.join(base_path, relative_path) - str
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def make_readme_file():
    """
    Description:
      - Creates a readme file if displaying AOS/LOS predicts.
      - Copies lines below to text file.
      - Saves the file.

    Output:
      ARISS_Clock_readme.txt.

    TODO (Readme File): Update as needed due to changes to the program.
    """
    # Text below is the contents of the readme file. Stylized after a man page.
    config_text = ['ARISS Clock Version ' + Ver + ' was written for Python 3.x on Linux.',
                   '',
                   'NAME',
                   '    ARISS_Clock - Simple readable large clock to support ISS',
                   '        passes in support of ARISS school contacts at ground ',
                   '        station K6DUE.',
                   '',
                   'SYNOPSIS',
                   '    Executable',
                   '        ARISS_Clock [ -b ] [ -c ] [ -h ] [ -l ] [ -s ] [ -t ]',
                   '',
                   '    Python script',
                   '        python ARISS_Clock.py [ -b ] [ -c ] [ -h ] [ -l ] [ -s ] [ -t ]',
                   '',
                   'DESCRIPTION',
                   '    Rise and Set times are set in the configuration file. As the Rise',
                   '    approaches the timer changes colors. At Rise the Rise timer stops',
                   '    at zero and the Set and Elapse Time (ET) timers start. The Set timer',
                   '    changes colors as Set is approached. At Set the Set timer and ET',
                   '    timers stop.',
                   '',
                   '    There are several clocks that are displayed. The Local Time (LT) zone',
                   '    is detected for the local time clock. A UTC clock is displayed next.',
                   '    Finally, there is a optional local school time clock. The School Time',
                   '    Zone (STZ) UTC time zone offset is specified in the config file. This',
                   '    clock label is fixed as Local School Time (LST).',
                   '',
                   'COMMAND LINE OPTIONS',
                   '    -b, -B, --BW',
                   '        Force Rise/Set timers to use only black & white colors.',
                   '        Default is to use color for active timers.',
                   '',
                   '    -c, -C, --Color',
                   '        Force background colors off.',
                   '        Default is color.',
                   '',
                   '    -h, -H, --Help',
                   '        Lists the command line options in terminal window, then exits.',
                   '        This will override all other command line options.',
                   '',
                   '    -l, -L, --Labels',
                   '        Turn OFF the display of the timer and clock labels.',
                   '        Default is to display the labels.',
                   '',
                   '    -s, -S, --School',
                   '        Turn OFF display Local School Time (LST) clock.',
                   '        Default is to display the clock.',
                   '',
                   '    -t, -T, --Top',
                   '        Remove timers from the top of the display and move to bottom.',
                   '        Default is to have timers at the top and clocks on bottom.',
                   '',
                   '    If any option is invalid the program uses all the defaults.',
                   '',
                   'EXAMPLES',
                   '    python ARISS_Clock.py or python3 ARISS_Clock.py',
                   '        Run the script from python using look and feel defaults.',
                   '',
                   '    python ARISS_Clock.py -l',
                   '        Run the script from python with labels not displayed.',
                   '',
                   '    python ARISS_Clock.py -T',
                   '        Run the script from python with the timers to the bottom of',
                   '        the display.',
                   '',
                   '    python ARISS_Clock.py --BW',
                   '        Run the script from python with black & white timers, no colors.',
                   '',
                   '    python ARISS_Clock.py -l -t -b',
                   '        Run the script from python with all command line options. Order',
                   '        does not matter. Can be upper and lower case. See above.',
                   '',
                   '    ARISS_Clock -l -t -b',
                   '        Run the executable with all command line options. The executable',
                   '        can use all the command line options that same way as the python',
                   '        script. A native executable not available for all operating systems.',
                   '',
                   'OVERVIEW',
                   '    Predicted Rise and Set times can be viewed in a separate window by',
                   '    clicking on the \"ARISS Contact Clock\" button. Rise and Set predicted',
                   '    date/times are displayed in local and UTC. These should be verified',
                   '    against the satellite tracking software. Edit the config file if',
                   '    incorrect and restart the ARISS Clock.',
                   '',
                   '    The Rise countdown timer only shows the hours, minutes, and seconds.',
                   '    If Rise is more than 24 hours away, the Rise will get to zero and',
                   '    roll over. If Rise and Set have already passed when the script is',
                   '    started, the Rise, Set, and ET timers will all show zero. The timers',
                   '    change color over time as Rise and Set are reached, unless the -b',
                   '    command line option was used.',
                   '',
                   '    Timer colors change based on the time matching the config file',
                   '    Rise and Set times.',
                   '',
                   '    Rise and Set timer colors change as follows:',
                   '        Rise starts off GREEN when active.',
                   '        Set and ET start off grayed out while Rise is not zero.',
                   '        Rise goes YELLOW at less than ' + str(int(yellow_alert/60)) + ' minutes to go. Warning!',
                   '        Rise goes RED at less than ' + str(int(red_alert/60)) + ' minute(s) to go. Red alert!',
                   '        Rise goes GRAY at zero. The contact has started.',
                   '        Set starts off YELLOW when active. Contact in progress.',
                   '        Set goes RED at less than ' + str(int(red_alert/60)) + ' to go. Red alert!',
                   '        Set goes GRAY at zero when Set is reached. Contact has ended.',
                   '',
                   '    Clock window can be resized. Fonts are scaled based on window width.',
                   '    To shrink, recommend adjusting the width first, then the height.',
                   '    To enlarge, recommend adjusting the height first, then the width.',
                   '',
                   '    Clocks or timers at the bottom of the display can be rolled up and ',
                   '    hidden from view. Grab the bottom the window and drag up. Expand the',
                   '    window to expose.',
                   '',
                   '    Rise time is checked to make sure it is before the Set time. If not,',
                   '    an error message comes up. For setting the Rise and Set times, the',
                   '    date matters. The Rise and Set timers will not change unless the date',
                   '    and time matches the UTC time clock. UTC is calculated based on the ',
                   '    system\'s time zone information read from the operating system.',
                   '',
                   'FONTS',
                   '    This script tries to use the "DejaVu Sans Mono" non-proportional',
                   '    font. Not all systems may have this font. If the specified font is',
                   '    not found it gets substituted with a different font and this will',
                   '    affect the look and feel. It is strongly recommend to install the ',
                   '    correct fonts. The fonts are free. See INTERNET RESOURCES below.',
                   '',
                   '    Required font files:',
                   '        DejaVuSansMono.ttf',
                   '        DejaVuSansMono-Bold.ttf',
                   '',
                   'FILES AND DIRECTORIES',
                   '    All the files should be in the same folder.',
                   '',
                   '    ARISS_Clock.py',
                   '        Python script. Main program. Requires python 3.x to run.',
                   '        Requires a number of Python libraries that may not be included',
                   '        with Python by default. Use pip to install.',
                   '',
                   '    ARISS_Clock.exe (may not be included)',
                   '        Windows executable version of main program.',
                   '',
                   '    ARISS_Clock_config.txt',
                   '        The Rise and Set times and school time zone are set in the',
                   '        configuration file. Instructions are included in the file. At',
                   '        startup the configuration file is read. If the config file is',
                   '        not found in the same folder as the program,a new config file',
                   '        is created and the Rise and Set times will need to be updated.',
                   '',
                   '        Verify configuration file version matches the ARISS Clock version.',
                   '        If not, delete the configuration file and restart. A new file will',
                   '        be generated with default values Edit for new school time zone ',
                   '        offset, Rise and Set date/times.',
                   '',
                   '        If the configuration file gets corrupted, just delete it, and',
                   '        restart the ARISS Clock. A new file will be created.',
                   '',
                   '    ARISS_Clock_readme.txt',
                   '        This help file. The file is generated every time the program is',
                   '        started up.',
                   '',
                   '    ARISS_logo.png',
                   '        ARISS logo image used by the python script. Must be present if',
                   '        running the .py file. Built into the executable.',
                   '',
                   '    ARISS_logo_simple.ico',
                   '        ARISS logo icon image. Used by Windows.',
                   '',
                   'AUTHOR',
                   '    By Ken McCaughey (N3FZX) for the K6DUE ARISS ground station.',
                   '    Copyright 2024.',
                   '',
                   'INTERNET RESOURCES',
                   '   DejaVu Fonts at https://dejavu-fonts.github.io or from',
                   '   1001 Fonts at https://www.1001fonts.com/dejavu-sans-mono-font.html',
                   '']
    # Create readme file.
    with open(file_readme, 'w') as f:
        for text_line in config_text:
            f.write(text_line)
            f.write('\n')


def report_config():
    """
    Description:
      - Report on configuration file creation.
      - Creates a window with a message that the file was created.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report Config): None.
    """
    # Message that config file was not found and a new one created.
    message = tk.Tk()  # Create a window.
    message.title('ARISS Clock Error')  # Window title.
    message.geometry('400x240')  # Initial size of window. Can be resized.
    img = tk.PhotoImage(file=resource_path('ARISS_logo.png'))
    if platform.system() == 'Windows':
        message.wm_iconbitmap(default=resource_path('ARISS_logo_simple.ico'))
        # x = 1
    else:
        message.wm_iconphoto(True, img)  # Window top left corner icon.
    message = tk.Label(message,
                       text='Configuration File Missing!\r'
                            'Created New Config File\r '
                            'ARISS_Clock_config.txt\r\r '
                            'Please edit config file with\r'
                            'new RISE/SET date/times,\r'
                            'then restart ARISS_Clock.\r\r'
                            'Close this window to continue.\r',
                       font=(text_font, 15, 'bold'),
                       fg='red')
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def make_config_file():
    """
    Description:
      - Creates a default configuration file.
      - Copies lines from config text to text file.
      - Saves the file.
      - Can call a function to display a window with a message that the file was created.

    Output:
      ARISS_Clock.txt.

    TODO (Make Config): None.
    """
    config_text = ['# ARISS Clock Config File',
                   '#',
                   '# Used by ARISS_Clock Version ' + Ver,
                   '#',
                   '# Verify the above version number matches the ARISS Clock version.',
                   '# If not, delete the config file and restart ARISS Clock.',
                   '# A new config file will be generated with default values.',
                   '#',
                   '# This file must be in same folder as executable or main script.',
                   '# This file must be named ARISS_Clock_config.txt.',
                   '# All comment lines must begin with a \'#\' character.',
                   '#',
                   '# For the optional Local School Time (LST) clock, enter the',
                   '# School Time Zone (STZ) with respect to UTC in this format only:.',
                   '#   STZ,+HH (HH is hours offset from UTC preceded with +/-.)',
                   '# For example:',
                   '#   STZ,-5',
                   '#   STZ,-2.5',
                   '#',
                   '# Predicted RISE (RS) & SET (ST) UTC dates/times in this format only:',
                   '#   RS,YYYY-MM-DD HH:mm:ss',
                   '#   ST,YYYY-MM-DD HH:mm:ss',
                   '# For example:',
                   '#   RS,' + Rel_date + ' 01:23:45',
                   '#   ST,' + Rel_date + ' 12:34:56',
                   '# Can stage multiple Rise/Set pairs, but only one pair can be ',
                   '#   uncommented at a time.',
                   '#',
                   '#--------------------------------------------------------------------',
                   '#',
                   'STZ,-5',
                   'RS,' + Rel_date + ' 12:00:00',
                   'ST,' + Rel_date + ' 12:10:00']
    # Create config file.
    with open(file_config, 'w') as f:
        for text_line in config_text:
            f.write(text_line)
            f.write('\n')


def report_rise_set():
    """
    Description:
      - Report Rise and Set read from configuration file.
      - Creates message window with ARISS logo and the Rise and Set times.
      - Use this or report_rise_set_readme().
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report Rise/Set): None.
    """
    # Rise title.
    message = tk.Toplevel()  # Create a window.
    message.title('ARISS Clock Rise/Set Predicts')  # Window title.
    message.geometry('420x440')  # Initial size of window. Can be resized.
    img = tk.PhotoImage(file=resource_path('ARISS_logo.png'))
    if platform.system() == 'Windows':
        message.wm_iconbitmap(default=resource_path('ARISS_logo_simple.ico'))
        # x = 1
    else:
        message.wm_iconphoto(True, img)  # Window top left corner icon.
    logo = tk.Label(message, image=img)  # Show ARISS logo. Sized will be fixed.
    message_rise_title = tk.Label(message,
                                  text='Predicted Rise Time',
                                  font=(text_font, 15, 'bold'))
    # Predicted Rise in UTC time.
    message_rise_utc_predict = tk.Label(message,
                                        text=rise_utc + ' UTC',
                                        font=(text_font, 15))
    # Predicted Rise in local time.
    message_rise_predict = tk.Label(message,
                                    text=rise_local + ' LT ',
                                    font=(text_font, 15))

    # Set title.
    message_set_title = tk.Label(message,
                                 text='Predicted Set Time',
                                 font=(text_font, 15, 'bold'))
    # Predicted Set in UTC time.
    message_set_utc_predict = tk.Label(message,
                                       text=set_utc + ' UTC',
                                       font=(text_font, 15))
    # Predicted Set in local time.
    message_set_predict = tk.Label(message,
                                   text=set_local + ' LT ',
                                   font=(text_font, 15))

    # Display window elements.
    logo.pack(padx=5, pady=5)
    message_rise_title.pack(padx=5, pady=5)
    message_rise_utc_predict.pack(padx=0, pady=0)
    message_rise_predict.pack(padx=0, pady=0)
    message_set_title.pack(padx=5, pady=5)
    message_set_utc_predict.pack(padx=0, pady=0)
    message_set_predict.pack(padx=0, pady=0)
    message.mainloop()


def report_rise_set_readme():
    """
    Description:
      - Report Rise and Set read from configuration file.
      - Combines the Rise/Set date/time check and the readme messages.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report AOS/LOS Readme): None.
    """
    # Rise title.
    # global my_img
    message = tk.Tk()  # Create a window.
    message.title('ARISS Clock Welcome')  # Window title.
    message.geometry('420x650')  # Initial size of window. Can be resized.
    img = tk.PhotoImage(file=resource_path('ARISS_logo.png'))
    if platform.system() == 'Windows':
        message.wm_iconbitmap(default=resource_path('ARISS_logo_simple.ico'))
        # x = 1
    else:
        message.wm_iconphoto(True, img)  # Window top left corner icon.
    logo = tk.Label(message, image=img)  # Show ARISS logo. Sized will be fixed.
    message_rise_title = tk.Label(message,
                                  text='Predicted Rise Time',
                                  font=(text_font, text_small, 'bold'))
    # Predicted Rise in UTC time.
    message_rise_utc_predict = tk.Label(message,
                                        text=rise_utc + ' UTC',
                                        font=(text_font, text_small))
    # Predicted Rise in local time.
    message_rise_predict = tk.Label(message,
                                    text=rise_local + ' LT ',
                                    font=(text_font, text_small))

    # Set title.
    message_set_title = tk.Label(message,
                                 text='Predicted Set Time',
                                 font=(text_font, text_small, 'bold'))
    # Predicted Set in UTC time.
    message_set_utc_predict = tk.Label(message,
                                       text=set_utc + ' UTC',
                                       font=(text_font, text_small))
    # Predicted Set in local time.
    message_set_predict = tk.Label(message,
                                   text=set_local + ' LT ',
                                   font=(text_font, text_small))
    #
    message1 = tk.Label(message,
                        text='Confirm RISE & SET times from\r'
                             'the config file. If incorrect\r'
                             'edit ARISS_Clock_config.txt  \r',
                             # 'Close this window to continue.\r',
                        font=(text_font, text_small, 'bold'),
                        fg='red')  # Message text.
    logo.pack(padx=5, pady=5)
    message1.pack(padx=5, pady=5)  # Display message.
    message_rise_title.pack(padx=5, pady=5, fill='both')  # Display Rise title.
    message_rise_utc_predict.pack(padx=0, pady=0)  # Display predicted Rise time in UTC.
    message_rise_predict.pack(padx=0, pady=0)  # Display predicted Rise time in local time.
    message_set_title.pack(padx=5, pady=5)  # Display Set title.
    message_set_utc_predict.pack(padx=0, pady=0)  # Display predicted Set time in UTC.
    message_set_predict.pack(padx=0, pady=0)  # Display predicted Set time in local time.
    message2 = tk.Label(message,
                        text='See ARISS_Clock_readme.txt    \r'
                             'for features and information  \r'
                             'on how to use this program.   \r\r'
                             'Close this window to continue.\r',
                        font=(text_font, text_small, 'bold'),
                        fg='red')  # Message text.
    message2.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_rise_error():
    """
    Description:
      - Reports Rise time error.
      - Creates a window with an error message.
      - AOS either not found, or incorrect format.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report AOS Error): None.
    """
    message = tk.Tk()  # Create a window.
    message.title('ARISS Clock Error')  # Window title.
    message.geometry('400x170')  # Initial size of window. Can be resized.
    message = tk.Label(message,
                       text='Configuration File Error!\r'
                            'RISE time in incorrect format.\r'
                            'Please edit config file with\r'
                            'new RISE date/times\r '
                            'then restart ARISS_Clock.\r'
                            'Close this window to continue.\r',
                       font=(text_font, text_small, 'bold'),
                       fg='red')  # Message text.
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_set_error():
    """
    Description:
      - Reports Set time error.
      - Creates a window with an error message.
      - LOS either not found, or incorrect format.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report LOS Error): None.
    """
    message = tk.Tk()  # Create a window.
    message.title('ARISS Clock Error')  # Window title.
    message.geometry('400x170')  # Initial size of window. Can be resized.
    message = tk.Label(message,
                       text='Configuration File Error!\r'
                            'SET time in incorrect format.\r'
                            'Please edit config file with\r'
                            'new SET date/times\r '
                            'then restart ARISS_Clock.\r'
                            'Close this window to continue.\r',
                       font=(text_font, text_small, 'bold'),
                       fg='red')  # Message text.
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_time_check_error():
    """
    Description:
      - Reports Rise/Set error.
      - Creates a window with an error message that Set is before Rise.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report Time Check Error): None.
    """
    message = tk.Tk()  # Create a window.
    message.title('ARISS Clock Error')  # Window title.
    message.geometry('400x170')  # Initial size of window. Can be resized.
    message = tk.Label(message,
                       text='Configuration File Error!\r'
                            'SET is before RISE time.\r'
                            'Please edit config file with\r'
                            'new RISE/SET date/times\r '
                            'then restart ARISS_Clock.\r'
                            'Close this window to continue.\r',
                       font=(text_font, text_small, 'bold'),
                       fg='red')  # Message text.
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def time_zone():
    """
    Description:
      - Get local time zone.
      - Uses regular expression to get time zone abbreviation.
      - %Z reports time zone abbreviated name, ie. EST.
      - Windows spells out the time zone instead of three letter abbreviation.
      - This pulls out the capitalized first letters. Works in Linux & Win.
      - Most time zones have a three letter abbreviation, but some are four.
      - Updated every 100ms.

    Output:
      Abbreviated local zone zone.

    TODO (Time Zone): None.

    :return: abbreviated_tz_str - str
    """
    current_time = time.strftime('%H:%M:%S %Z')  # Get time. Format time per mask.
    abbreviated_tz_str = re.sub(r'[^A-Z]', '', current_time)  # Get first letter in caps.
    return abbreviated_tz_str  # Local time zone.


def scale_font():
    """
    Description:
      - Scale the fonts.
      - Changes font size based on window width.

    Output:
      text_large, text_med, text_small, text_smaller

    TODO (Scale Font): None.
    """
    global text_large
    global text_med
    global text_small
    global text_smaller
    global root
    # aspect_ratio = window_height / window_width
    win_width = root.winfo_width()
    scale = (win_width / window_width)
    text_large = int(40 * scale)
    text_med = int(25 * scale)
    text_small = int(15 * scale)
    text_smaller = int(10 * scale)
    # Display text elements listed in order from top to bottom.
    title_button.config(font=(text_font, text_med, 'bold'), width=win_width)
    hms_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    clock_local_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    clock_local.config(font=(text_font, text_large, 'bold'), width=win_width)
    clock_utc_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    clock_utc.config(font=(text_font, text_large, 'bold'), width=win_width)
    clock_school_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    clock_school.config(font=(text_font, text_large, 'bold'), width=win_width)
    timer_rise_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    timer_rise.config(font=(text_font, text_large, 'bold'), width=win_width)
    timer_set_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    timer_set.config(font=(text_font, text_large, 'bold'), width=win_width)
    timer_pass_elapsed_time_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    timer_pass_elapsed_time.config(font=(text_font, text_large, 'bold'), width=win_width)
    notice.config(font=(text_font, text_smaller), width=win_width)


def time_local():
    """
    Description:
      - Calls scale_font()
      - Get local time.
      - Formats local time for display.
      - %Z reports time zone abbreviated name, ie. EST.
      - Windows spells out the time zone instead of three letter abbreviation.
      - This pulls out the capitalized first letters. Works in Linux & Win.
      - Updated every 100ms.

    Output:
      clock_local

    TODO: (Local Time) None.
    """
    # current_time = time.strftime('%H:%M:%S %Z')  # Get time. Format time per mask.
    # abbreviated_tz_str = re.sub(r'[^A-Z]', '', current_time)  # Get first letter in caps.
    scale_font()  # Call the function to scale fonts.
    abbreviated_tz_str = time_zone()  # Get local time zone.
    current_time = time.strftime(' %H:%M:%S ')  # Re-read local time w/o time zone.
    # current_time = current_time + abbreviated_tz_str + ' '  # Add abbreviated time zone.
    current_time = current_time + 'LT   '  # Add abbreviated time zone.
    clock_local.config(text=current_time)  # Convert to text.
    clock_local.after(100, time_local)  # Updated every 100ms.


def time_utc():
    """
    Description:
      - Get UTC time.
      - Formats UTC time for display.
      - Updated every 100ms.

    Output:
      clock_utc

    TODO (UTC Time): None.
    """
    # utc_datetime = datetime.utcnow()  # Get time.
    utc_datetime = datetime.now(timezone.utc).replace(tzinfo=None)  # Get time.
    current_time_utc = utc_datetime.strftime(' %H:%M:%S UTC  ')  # Format time per mask.
    clock_utc.config(text=current_time_utc)  # Convert to text.
    clock_utc.after(100, time_utc)  # Updated every 100ms.


def time_school():
    """
    Description:
      - Get school local time time.
      - Uses school time zone UTC offset.
      - Formats school time for display.
      - Time label is fixed as LST.
      - Updated every 100ms.

    Output:
      clock_school

    TODO (School Time): None.
    """
    global stz
    # Get time and add UTC offset from config file.
    utc_datetime = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=stz)
    current_time_school = utc_datetime.strftime(' %H:%M:%S LST  ')  # Format time per mask.
    clock_school.config(text=current_time_school)  # Convert to text.
    clock_school.after(100, time_school)  # Updated every 100ms.


def time_rise():
    """
    Description:
      - Rise countdown time.
      - Uses Rise time read from config file.
      - Formats Rise time for display. Will stop at zero.
      - Updated every 100ms.

    Output:
      clock_aos

    TODO (Time Rise): None.
    """
    # Difference between current local time and Rise UTC time.
    # delta = rise - time.time() - time.timezone + (time.daylight * 3600) + 1
    delta = rise - time.time() - time.timezone + 1
    if delta <= yellow_alert:
        timer_rise['bg'] = rise_color_warning  # Change background color.
        timer_rise_label['bg'] = rise_color_warning  # Change background color.
    if delta <= red_alert:
        timer_rise['bg'] = rise_color_alert  # Change background color.
        timer_rise_label['bg'] = rise_color_alert  # Change background color.
    if delta >= 1:  # Update Rise time if Rise is not yet been reached.
        timer_rise['text'] = time.strftime(' %H:%M:%S Rise ', time.localtime(delta + (5 * 3600)))
    else:
        timer_rise['text'] = ' 00:00:00 Rise '  # Show zero when delta is negative.
        timer_rise['bg'] = aos_color_stopped  # Change background color when AOS is reached.
        timer_rise_label['bg'] = aos_color_stopped  # Change background color.
    timer_rise.config(font=(text_font, text_large, 'bold'))
    timer_rise.after(100, time_rise)  # Updated every 100ms.


def time_set():
    """
    Description:
      - Set countdown time.
      - Uses Set time read from config file.
      - Formats Set time for display. Will stop at zero.
      - Updated every 100ms.

    Output:
      clock_los

    TODO (Time Set): None.
    """
    # Rise trigger to start ET.
    # delta1 = rise - time.time() - time.timezone + (time.daylight * 3600) + 1
    delta1 = rise - time.time() - time.timezone + 1
    # Difference between current local time and LOS time.
    # delta2 = Set - time.time() - time.timezone + (time.daylight * 3600) + 1
    delta2 = Set - time.time() - time.timezone + 1
    if (delta1 >= 0) & (delta2 >= 0):
        # clock_los['text'] = ' 00:00:00 Set  '  # Display before AOS.
        timer_set['text'] = '    __:__ Set  '  # Display before AOS.
        timer_set['bg'] = gray  # Change background color.
        timer_set_label['bg'] = gray  # Change background color.
    if (delta1 <= 1) & (delta2 >= 1):  # Update Set time if Set is not yet been reached.
        # clock_set['text'] = time.strftime('%H:%M:%S Set', time.localtime(delta2 + (5 * 3600)))  # Shows HH:mm:ss.
        timer_set['text'] = time.strftime('    %M:%S Set  ', time.localtime(delta2 + (5 * 3600)))  # Shows only mm:ss.
        if delta2 <= red_alert:
            timer_set['bg'] = set_color_alert
            timer_set_label['bg'] = set_color_alert
        else:
            timer_set['bg'] = set_color_started  # Change background color after Rise.
            timer_set_label['bg'] = set_color_started  # Change background color after Rise.
    elif delta2 <= 1:
        # clock_set['text'] = ' 00:00:00 Set  '  # Show zero when delta is negative.
        timer_set['text'] = '    00:00 Set  '  # Show zero when delta is negative.
        timer_set['bg'] = set_color_stopped  # Change background color is Set has occurred.
        timer_set_label['bg'] = set_color_stopped  # Change background color is Set has occurred.
    timer_set.after(100, time_set)  # Updated every 100ms.


def time_pass_elapsed():
    """
    Description:
      - AOS elapsed time.
      - Uses Rise and Set time read from config file.
      - Calculates and formats elapsed time for display. Start at zero.\
      - Starts when AOS is zero, stops when LOS is zero.
      - Updated every 100ms.

    Output:
      clock_pass

    TODO (Pass Times): None.
    """
    # delta1 = rise - time.time() - time.timezone + (time.daylight * 3600) + 1  # Rise trigger to start ET.
    delta1 = rise - time.time() - time.timezone + 1  # Rise trigger to start ET.
    # delta2 = Set - time.time() - time.timezone + (time.daylight * 3600) + 1  # Set trigger to stop ET.
    delta2 = Set - time.time() - time.timezone + 1  # Set trigger to stop ET.
    delta3 = time.time() - rise  # Calculate elapsed time since AOS.
    if delta1 >= 1:
        # clock_pass['text'] = ' 00:00:00 ET  '  # ET display before Rise.
        timer_pass_elapsed_time['text'] = '    __:__ ET   '  # ET displayed before Rise.
    elif delta2 >= 0:  # Rise trigger to start ET.
        # Shows HH:mm:ss.
        # timer_pass_elapsed_time['text'] = time.strftime(' %H:%M:%S ET  ', time.localtime(delta3 + (5 * 3600)))
        # Shows only mm:ss.
        timer_pass_elapsed_time['text'] = time.strftime('    %M:%S ET   ', time.localtime(delta3 + (5 * 3600)))
        timer_pass_elapsed_time['bg'] = pass_elapsed_time_color  # Change background color after Rise.
        timer_pass_elapsed_time_label['bg'] = pass_elapsed_time_color  # Change background color after Rise.
    timer_pass_elapsed_time.after(100, time_pass_elapsed)  # Updated every 100ms.


# ========================================================================
# MAIN
# ========================================================================

make_readme_file()  # Call the function to create readme file.
startup()  # Call the function to read and parse command line options.


# --- Read configuration data from file. ---------------------------------

# This is done one time when the script is started.
# Config file can use '#' for comments.
# ISS Rise and Set times are in local ground station time in this exact format only:
#   RS,YYYY-MM-DD HH:mm:ss
#   ST,YYYY-MM-DD HH:mm:ss
try:
    a_file = open(file_config)                 # Open configuration text file.
except FileNotFoundError:                      # If file not found error, create one.
    make_config_file()                         # Call the function to create config file.
    report_config()                            # Call the function to report creation of config file.
    a_file = open(file_config)                 # Open new configuration text file.
for line in a_file:                            # Loop through eac line in text file.
    if not line.startswith('#'):               # Ignore comment lines starting with '#'.
        key, value = line.split(',')           # Separate keys from values based on comma.
        a_dictionary[key] = value.strip('\n')  # Load dictionary. Remove newlines from values.


# --- Time zones. --------------------------------------------------------

tz = time_zone()  # Call the function to calculate local time zone.
# School local time zone. Read UTC offset from config file.
try:
    STZ = a_dictionary['STZ']
#    stz = int(STZ)
    stz = float(STZ)
except KeyError:
    a_dictionary['STZ'] = '0'  # Set default AOS
    STZ = a_dictionary['STZ']
#    stz = int(STZ)
    stz = float(STZ)


# --- AOS time. ----------------------------------------------------------

# Check for missing or incorrect AOS time in config file.
try:
    RISE = a_dictionary['RS']  # Read Rise date/time.
except KeyError:
    report_rise_error()  # Call the function to report error.
    a_dictionary['RS'] = '2021-01-01 00:00:00'  # Set default Rise
    RISE = a_dictionary['RS']  # Read Rise date/time.
try:
    RISE = tuple([int(x) for x in RISE[:10].split('-')]) + tuple([int(x) for x in RISE[11:].split(':')])
    rise = datetime(*RISE).timestamp()  # Convert tuple.
except ValueError:
    report_rise_error()  # Call the function to report error.
    a_dictionary['RS'] = '2021-01-01 00:00:00'  # Set default Rise
    RISE = a_dictionary['RS']  # Read Rise date/time.
    RISE = tuple([int(x) for x in RISE[:10].split('-')]) + tuple([int(x) for x in RISE[11:].split(':')])
    rise = datetime(*RISE).timestamp()  # Convert tuple.
# rise_utc = datetime.fromtimestamp(rise, tz=timezone.utc)  # Convert local Rise time to UTC.
rise_utc = datetime.fromtimestamp(rise)
rise_utc = rise_utc.strftime('%Y-%m-%d %H:%M:%S')

# Compute Rise in local time base on UTC time in config file.
# rise_local = rise - time.timezone + (time.daylight * 3600)
rise_local = rise - time.timezone
rise_local = datetime.fromtimestamp(rise_local)
rise_local = rise_local.strftime('%Y-%m-%d %H:%M:%S')
# print("Rise Local ", rise_local)

# --- LOS time. ----------------------------------------------------------

# Check for missing or incorrect Set time in config file.
try:
    SET = a_dictionary['ST']  # Read LOS date/time.
except KeyError:
    report_rise_error()  # Call the function to report error.
    a_dictionary['ST'] = '2021-01-01 01:00:00'  # Set default SetS
    SET = a_dictionary['ST']  # Read Set date/time.
try:
    SET = tuple([int(x) for x in SET[:10].split('-')]) + tuple([int(x) for x in SET[11:].split(':')])
    Set = datetime(*SET).timestamp()  # Convert tuple.
except ValueError:
    report_set_error()  # Call the function to report error.
    a_dictionary['ST'] = '2021-01-01 01:00:00'  # Set default Set
    SET = a_dictionary['ST']  # Read Set date/time.
    SET = tuple([int(x) for x in SET[:10].split('-')]) + tuple([int(x) for x in SET[11:].split(':')])
    Set = datetime(*SET).timestamp()  # Convert tuple.
# set_utc = datetime.fromtimestamp(Set, tz=timezone.utc)  # Convert local Set time to UTC.
set_utc = datetime.fromtimestamp(Set)
set_utc = set_utc.strftime('%Y-%m-%d %H:%M:%S')

# Compute Set in local time base on UTC time in config file.
# set_local = Set - time.timezone + (time.daylight * 3600)
set_local = Set - time.timezone
set_local = datetime.fromtimestamp(set_local)
set_local = set_local.strftime('%Y-%m-%d %H:%M:%S')
# print("Set Local  ", set_local)

# --- Check that AOS is before LOS. --------------------------------------

if rise_utc > set_utc:
    report_time_check_error()  # Call the function to report Rise/Set error message window.


# --- Report predicted Rise and Set date/times. ---------------------------

# Show predicted Rise/Set times to be verified in a separate window.
report_rise_set_readme()  # Call the function to report Rise and Set predicts and readme.


# --- Debug for parameters read from config file. ------------------------

# Can comment out if it is working.
# print(a_dictionary)  # Show dictionary.
# print('STZ:', a_dictionary['STZ'])
# print(stz)
# print('Rise LOC:', a_dictionary['RS'])
# print('Rise UTC:', aos_utc)
# print(RISE)
# print(rise)
# print('Set LOC:', a_dictionary['ST'])
# print('Set UTC:', los_utc)
# print(SET)
# print(Set)


# --- Display color management. ------------------------------------------

# Color map. Comment out alternate colors.
red = 'indianred1'
# red = 'palevioletred1'
yellow = 'lightgoldenrod1'
# yellow = 'yellow1'
green = 'palegreen1'
# green = 'indianred1'
gray = 'gray60'
orange = 'orange1'
bw = 'grey75'  # Color for black and white command line option. 'grey85' matches window.
# bw = 'grey85'  # Color for black and white command line option. 'grey85' matches window.

# Window colors.
window_background = 'gray85'
title_button_color = 'gray60'
text_color = 'gray0'
# text_color = 'white'

# Clock background (bg) and foreground (fg) color settings.
clock_local_color_bg = 'white'
clock_local_color_fg = 'gray0'
clock_utc_color_bg = 'gray0'
clock_utc_color_fg = 'white'
clock_school_color_bg = 'gray60'
clock_school_color_fg = 'gray0'

# Set colors based on command line options.
if timer_color:  # -b option.
    red = bw
    yellow = bw
    green = bw
    orange = bw
    #
    window_background = 'gray85'
    title_button_color = gray
    text_color = 'gray0'
if background_color:  # -c option.
    # window_background = 'steelblue2'
    window_background = '#0F6DB1'
    title_button_color = 'gold'
    # text_color = 'gray0'
    text_color = 'white'
aos_color_started = green  # Timer is running.
rise_color_warning = yellow  # Time at six minute to Rise. Warning!
rise_color_alert = red  # Time at one minute to Rise. Read alert!
aos_color_stopped = gray  # Timer stopped.
set_color_started = yellow  # Timer is running. Warning!
set_color_alert = red  # Time at one minute to Set. Red alert!
set_color_stopped = gray  # Timer stopped.
pass_elapsed_time_color = orange  # Elapsed time after Rise.


# --- Create display window. ---------------------------------------------

window_size, window_width = set_window_height()
# print(window_size)
root = tk.Tk()  # Create a window.
root.title('ARISS Clock')  # Window title.
root.geometry(window_size)  # Initial size of window. Can be resized.
my_img = tk.PhotoImage(file=resource_path('ARISS_logo.png'))
if platform.system() == 'Windows':
    root.wm_iconbitmap(default=resource_path('ARISS_logo_simple.ico'))
    # x = 1
else:
    root.wm_iconphoto(True, my_img)  # Window top left corner icon.
root.configure(bg=window_background)  # Option to change window background color. If used need to check text bg colors.


# --- Configure widgets. -------------------------------------------------

# Using non-proportional fonts.
#   Not all systems may have these fonts.
#   Using a different font may require tweaking of window size to restore look and feel.
#   Order does not matter here.

# Window title.
# logo = tk.Label(root,  image=my_img)  # Show ARISS logo. Sized will be fixed.
title_button = tk.Button(root,
                         text='ARISS Contact Clock',
                         font=(text_font, text_med, 'bold'),  # Title text.
                         activebackground='white', bg=title_button_color,
                         command=report_rise_set)
# Hours, min, sec labels.
hms_label = tk.Label(root, text="hrs     min     sec             ",
                     font=(text_font, text_small, 'bold'),
                     fg=text_color, bg=window_background)
# Local time clock.
clock_local = tk.Label(root,
                       font=(text_font, text_large, 'bold'),
                       bg=clock_local_color_bg, fg=clock_local_color_fg,
                       padx=20)
clock_local_label = tk.Label(root,
                             text='Local Time',
                             font=(text_font, text_small, 'bold'),
                             bg=clock_local_color_bg, fg=clock_local_color_fg,
                             padx=20)
# UTC clock.
clock_utc = tk.Label(root,
                     font=(text_font, text_large, 'bold'),
                     bg=clock_utc_color_bg, fg=clock_utc_color_fg,
                     padx=20)  # UTC clock.
clock_utc_label = tk.Label(root,
                           text='Universal Time Coordinated',
                           font=(text_font, text_small, 'bold'),
                           bg=clock_utc_color_bg, fg=clock_utc_color_fg,
                           padx=20)
# School clock.
clock_school = tk.Label(root,
                        font=(text_font, text_large, 'bold'),
                        bg=clock_school_color_bg, fg=clock_school_color_fg,
                        padx=20)
clock_school_label = tk.Label(root,
                              text='Local School Time',
                              font=(text_font, text_small, 'bold'),
                              bg=clock_school_color_bg, fg=clock_school_color_fg,
                              padx=20)
# Rise timer.
timer_rise = tk.Label(root,
                      font=(text_font, text_large, 'bold'),
                      bg=aos_color_started,
                      padx=20)
timer_rise_label = tk.Label(root,
                            text='Countdown to Rise Time',
                            font=(text_font, text_small, 'bold'),
                            bg=aos_color_started,
                            padx=20)
# Set timer.
timer_set = tk.Label(root,
                     font=(text_font, text_large, 'bold'),
                     bg=gray,
                     padx=20)
timer_set_label = tk.Label(root,
                           text='Countdown to Set Time',
                           font=(text_font, text_small, 'bold'))
# Pass elapsed time timer.
timer_pass_elapsed_time = tk.Label(root,
                                   text='    00:00 ET   ',  # ' 00:00:00 ET  '
                                   font=(text_font, text_large, 'bold'),
                                   bg=gray,
                                   padx=20)
timer_pass_elapsed_time_label = tk.Label(root,
                                         text='Pass Elapsed Time',
                                         font=(text_font, text_small, 'bold'),
                                         bg=gray,
                                         padx=20)
# Notice text.
notice = tk.Label(root,
                  text='Version ' + Ver + ' - By N3FZX for K6DUE',
                  font=(text_font, text_small),
                  fg=text_color, bg=window_background)


# --- Function calls to update clocks. -----------------------------------

time_local()         # Call the function to get local time.
time_utc()           # Call the function to get UTC time.
time_school()        # Call the function to get local school time.
time_rise()          # Call the function to get Rise time.
time_set()           # Call the function to get Set time.
time_pass_elapsed()  # Call the function to get pass elapsed time.


# --- Display clocks and text in window. ---------------------------------

# The order here defines the order displayed.
# Set label, then pack to display.

title_button.pack(padx=5, pady=(10, 5))  # Display title.
hms_label.pack(padx=5, pady=0)  # Display time labels.

if not display_rise_set_et_top:
    clock_local.pack(padx=5, pady=(10, 0))  # Display local clock. Label set in functions.
    if display_labels:
        clock_local_label.pack(padx=5, pady=(0, 2))  # Display local time.
    clock_utc.pack(padx=5, pady=(10, 0))  # Display UTC clock. Label set in functions.
    if display_labels:
        clock_utc_label.pack(padx=5, pady=(0, 2))  # Display UTC time.
    if show_school_clock:
        clock_school.pack(padx=5, pady=(10, 0))  # Display school clock. Label set in functions.
        if display_labels:
            clock_school_label.pack(padx=5, pady=(0, 2))  # Display school local time.

timer_rise.pack(padx=5, pady=(10, 0))  # Display Rise countdown clock.
if display_labels:
    timer_rise_label.pack(padx=5, pady=(0, 2), fill='both')  # Display Rise title.

timer_set.pack(padx=5, pady=(10, 0))  # Display Set countdown clock.
if display_labels:
    timer_set_label.pack(padx=5, pady=(0, 2), fill='both')  # Display Set title.

timer_pass_elapsed_time.pack(padx=5, pady=(10, 0))  # Display pass elapsed time.
if display_labels:
    timer_pass_elapsed_time_label.pack(padx=5, pady=(0, 2))  # Display pass elapsed time.

if display_rise_set_et_top:
    clock_local.pack(padx=5, pady=(10, 0))  # Display local clock. Label set in functions.
    if display_labels:
        clock_local_label.pack(padx=5, pady=(0, 2))  # Display local time.
    clock_utc.pack(padx=5, pady=(10, 0))  # Display UTC clock. Label set in functions.
    if display_labels:
        clock_utc_label.pack(padx=5, pady=(0, 2))  # Display UTC time.
    if show_school_clock:
        clock_school.pack(padx=5, pady=(10, 0))  # Display school clock. Label set in functions.
        if display_labels:
            clock_school_label.pack(padx=5, pady=(0, 5))  # Display pass elapsed time.

notice.pack(padx=5, pady=(10, 5))  # Display notice.

root.mainloop()  # Loop.

# The End
