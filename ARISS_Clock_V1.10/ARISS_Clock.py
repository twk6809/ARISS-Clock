# === ARISS_Clock.py =====================================================
"""
| NAME: ARISS Clock
| BY: Ken McCaughey (N3FZX)
| ON: 2024-09-04
| VERSION: 1.10
| STATUS: Final development version for V1.10.
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
    Reads school time zone UTC offset, ISS AOS and LOS times from a config
    file. Shows a countdown to AOS and LOS. Once AOS is zero, the pass
    elapsed time timer starts. This timer stops at LOS, showing the total
    elapsed time of the pass.
  - Uses local time for AOS and LOS. UTC and school times are for
    informational purposes only. All AOS/LOS events are triggered
    based on local time clock.
  - If AOS and LOS are more that 24 hours out, the time will roll
    over and the ET will not trigger. The date matters!
  - The window fonts can be resized by changing the width. Height can be
    changed as well, but it does not affect the font scaling. Can change
    height to rollup clock or timers from the bottom to hide them.
  - There is a button to view the predicted AOS/LOS date/times.
  - There is limited error checking included. Error message window reports
    missing or incorrect AOS/LOS time, or if AOS is after LOS. A
    default AOS/LOS is substituted.

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
    AOS and LOS date/times. Start program. Config file needs to be in
    same folder as executable.
  - Checks for missing or incorrect AOS and LOS from the config file.
    Opens a message window and uses default AOS/LOS date/times.
  - Checks that AOS is before LOS. If not it opens a message window.
  - There are a button to view the AOS/LOS predicts.

MAKING AN EXECUTABLE
  - Can be made into an executable using pyinstaller.
  - Will require files ARISS_logo_simple.png and ARISS_logo_simple.ico.
  - On Linux use command line:
      pyinstaller --onefile -w -F -i "ARISS_logo_simple.ico" --add-data 'ARISS_logo.png:.' ARISS_Clock.py
  - Windows 10 pyinstaller command line
      pyinstaller -w -F -i "ARISS_logo_simple.ico" --add-data ARISS_logo.png;. --add-data ARISS_logo_simple.ico;. ARISS_Clock.py
  - If a .spec files exists,on the command line enter: "pyinstaller ARISS_Clock.spec"

EXTERNAL CREDITS:
  - CREATE A GUI DIGITAL CLOCK USING TIME AND TKINTER LIBRARIES.
  - https://cppsecrets.com/users/218111411511410110199104971141051161049764103109971051084699111109/Python-GUI-Digital-Clock.php

TODO (Top Level):
 - Requires logo file to be present. Consider error checking if logo is missing.
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

Ver = '1.10'  # Version of this script.

# Command line option defaults.
#   If these are changed, update def startup() and the readme text in def make_readme_file().
timer_color = False            # -b option. Timer in black & white. Default = False. In color.
background_color = True        # -c option. Default = False. No color.
display_labels = True          # -l option. Show timer/clock labels. Default = False. Do not show.
show_school_clock = True       # -s option. Default = False. Do not show school clock.
display_aos_los_et_top = True  # -t option. Show AOS/LOS and ET clocks on top. Default = True. On top.

# When to change colors on timers in seconds before AOS.
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
a_dictionary = {'STZ': '0', 'AOS': '', 'LOS': ''}  # Dictionary default keys.


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
                    '"  -b, -B, --BW      AOS/LOS timers only in black and white."',
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
    global display_aos_los_et_top
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
                display_aos_los_et_top = False
    except getopt.error:
        timer_color = False             # -b option, default = False.
        background_color = True         # -c option, default = True.
        display_labels = True           # -l option, default = True.
        show_school_clock = True        # -s option, default = True
        display_aos_los_et_top = True   # -t option, default = True.
    # Uncomment to use for debugging.
    # except getopt.error as err:
    #     output error, and return with an error code
    #     print('Error:', str(err))
    #     display_predicts = False  # AOS/LOS predicts shown in main display?


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
    # Set geometry based on whether AOS/LOS is on main display, as set in config above.
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
                   '    AOS and LOS times are set in the configuration file. As the AOS',
                   '    approaches the timer changes colors. At AOS the AOS timer stops',
                   '    at zero and the LOS and ET timers start. The LOS timer changes',
                   '    colors as LOS is approached. At LOS the LOS timer and ET timers',
                   '    stop.',
                   '',
                   '    There are several clocks that are displayed. The local time zone',
                   '    is detected for the local time clock. A UTC clock is displayed next.',
                   '    Finally, there is a optional local school time clock. The School Time',
                   '    Zone (STZ) UTC time zone offset is specified in the config file. This',
                   '    clock label is fixed as Local School Time (LST).',
                   '',
                   'COMMAND LINE OPTIONS',
                   '    -b, -B, --BW',
                   '        Force AOS/LOS timers to use only black & white colors.',
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
                   '        Remove clocks from the top of the display and move to bottom.',
                   '        Default is to have them at the top.',
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
                   '        Run the script from python with the clocks to the bottom of',
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
                   '    Predicted AOS and LOS can be viewed in a separate window by',
                   '    clicking on the \"ARISS ISS Contact Clock\" button. AOS and LOS ',
                   '    predicted date/times are displayed in local and UTC. These should be',
                   '    verified against the satellite tracking software. Edit the config file',
                   '    if incorrect and restart the ARISS Clock.',
                   '',
                   '    The AOS countdown timer only shows the hours, minutes, and seconds.',
                   '    If AOS is more than 24 hours away, the AOS will get to zero and',
                   '    roll over. If AOS and LOS have already passed when the script is',
                   '    started, the AOS, LOS, and ET timers will all show zero. The timers',
                   '    change color over time as AOS and LOS are reached, unless the -b',
                   '    command line option was used.',
                   '',
                   '    Timer colors change based on the time matching the config file',
                   '    AOS and LOS times.',
                   '',
                   '    AOS and LOS timer colors change as follows:',
                   '        AOS starts off GREEN when active.',
                   '        LOS and ET start off grayed out while AOS is not zero.',
                   '        AOS goes YELLOW at less than ' + str(int(yellow_alert/60)) + ' minutes to go. Warning!',
                   '        AOS goes RED at less than ' + str(int(red_alert/60)) + ' minute(s) to go. Red alert!',
                   '        AOS goes GRAY at zero. The contact has started.',
                   '        LOS starts off YELLOW when active. Contact in progress.',
                   '        LOS goes RED at less than ' + str(int(red_alert/60)) + ' to go. Red alert!',
                   '        LOS goes GRAY at zero when LOS is reached. Contact has ended.',
                   '',
                   '    Clock window can be resized. Fonts are scaled based on window width.',
                   '    To shrink, recommend adjusting the width first, then the height.',
                   '    To enlarge, recommend adjusting the height first, then the width.',
                   '',
                   '    Clocks or timers at the bottom of the display can be rolled up and ',
                   '    hidden from view. Grab the bottom the window and drag up. Expand the',
                   '    window to expose.',
                   '',
                   '    AOS is checked to make sure it is before the LOS time. If not, an',
                   '    error message comes up. For setting the AOS and LOS times, the date',
                   '    matters. The AOS and LOS timers will not change unless the date and',
                   '    time matches the UTC time clock. UTC is calculated based on the ',
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
                   '        The AOS and LOS times and school time zone are set in the',
                   '        configuration file. Instructions are included in the file. At',
                   '        startup the configuration file is read. If the config file is',
                   '        not found in the same folder as the program,a new config file',
                   '        is created and the AOS and LOS times will need to be updated.',
                   '',
                   '        Verify configuration file version matches the ARISS Clock version.',
                   '        If not, delete the configuration file and restart. A new file will',
                   '        be generated with default values Edit for new school time zone ',
                   '        offset, AOS and LOS date/times.',
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
                   '    ARISS_Clock.spec (may not be included)',
                   '        File with preset parameters to create an executable version',
                   '        using \"pyinstaller\". Syntax is \"pyinstaller ARISS_Clock.spec\'.',
                   '',
                   'AUTHOR',
                   '    By Ken McCaughey (N3FZX) for the K6DUE ARISS ground station.',
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
                            'new AOS/LOS date/times,\r'
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
                   '# Predicted ISS AOS and LOS UTC dates and times in this format only:',
                   '#   AOS,YYYY-MM-DD HH:mm:ss',
                   '#   LOS,YYYY-MM-DD HH:mm:ss',
                   '# For example:',
                   '#   AOS,2022-02-08 01:23:45',
                   '#   LOS,2022-02-08 12:34:56',
                   '# Can stage multiple AOS/LOS pairs, but only one pair can be ',
                   '#   uncommented at a time.',
                   '#',
                   '#-------------------------------------------------------------------',
                   '#',
                   'STZ,-5',
                   'AOS,2024-09-04 12:00:00',
                   'LOS,2024-09-04 12:10:00']
    # Create config file.
    with open(file_config, 'w') as f:
        for text_line in config_text:
            f.write(text_line)
            f.write('\n')


def report_aos_los():
    """
    Description:
      - Report AOS and LOS read from configuration file.
      - Creates message window with ARISS logo and the AOS and LOS times.
      - Use this or report_aos_los_readme().
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report AOS): None.
    """
    # AOS title.
    message = tk.Toplevel()  # Create a window.
    message.title('ARISS Clock AOS/LOS Predicts')  # Window title.
    message.geometry('420x440')  # Initial size of window. Can be resized.
    img = tk.PhotoImage(file=resource_path('ARISS_logo.png'))
    if platform.system() == 'Windows':
        message.wm_iconbitmap(default=resource_path('ARISS_logo_simple.ico'))
        # x = 1
    else:
        message.wm_iconphoto(True, img)  # Window top left corner icon.
    logo = tk.Label(message, image=img)  # Show ARISS logo. Sized will be fixed.
    message_aos_title = tk.Label(message,
                                 text='Predicted Acquisition of Signal',
                                 font=(text_font, 15, 'bold'))
    # Predicted AOS in UTC time.
    message_aos_utc_predict = tk.Label(message,
                                       text=aos_utc + ' UTC',
                                       font=(text_font, 15))
    # Predicted AOS in local time.
    message_aos_predict = tk.Label(message,
                                   text=aos_local + ' LT ',
                                   font=(text_font, 15))

    # LOS title.
    message_los_title = tk.Label(message,
                                 text='Predicted Loss of Signal',
                                 font=(text_font, 15, 'bold'))
    # Predicted LOS in UTC time.
    message_los_utc_predict = tk.Label(message,
                                       text=los_utc + ' UTC',
                                       font=(text_font, 15))
    # Predicted LOS in local time.
    message_los_predict = tk.Label(message,
                                   text=los_local + ' LT ',
                                   font=(text_font, 15))

    # Display window elements.
    logo.pack(padx=5, pady=5)
    message_aos_title.pack(padx=5, pady=5)
    message_aos_utc_predict.pack(padx=0, pady=0)
    message_aos_predict.pack(padx=0, pady=0)
    message_los_title.pack(padx=5, pady=5)
    message_los_utc_predict.pack(padx=0, pady=0)
    message_los_predict.pack(padx=0, pady=0)
    message.mainloop()


def report_aos_los_readme():
    """
    Description:
      - Report AOS and LOS read from configuration file.
      - Combines the AOS/LOS date/time check and the readme messages.
      - Main ARISS_Clock window comes up after message window is closed.

    Output:
      Message window.

    TODO (Report AOS/LOS Readme): None.
    """
    # AOS title.
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
    message_aos_title = tk.Label(message,
                                 text='Acquisition of Signal',
                                 font=(text_font, text_small, 'bold'))
    # Predicted AOS in UTC time.
    message_aos_utc_predict = tk.Label(message,
                                       text=aos_utc + ' UTC',
                                       font=(text_font, text_small))
    # Predicted AOS in local time.
    message_aos_predict = tk.Label(message,
                                   text=aos_local + ' LT ',
                                   font=(text_font, text_small))

    # LOS title.
    message_los_title = tk.Label(message,
                                 text='Loss of Signal',
                                 font=(text_font, text_small, 'bold'))
    # Predicted LOS in UTC time.
    message_los_utc_predict = tk.Label(message,
                                       text=los_utc + ' UTC',
                                       font=(text_font, text_small))
    # Predicted LOS in local time.
    message_los_predict = tk.Label(message,
                                   text=los_local + ' LT ',
                                   font=(text_font, text_small))
    #
    message1 = tk.Label(message,
                        text='Confirm AOS & LOS times from \r'
                             'the config file. If incorrect\r'
                             'edit ARISS_Clock_config.txt  \r',
                             # 'Close this window to continue.\r',
                        font=(text_font, text_small, 'bold'),
                        fg='red')  # Message text.
    logo.pack(padx=5, pady=5)
    message1.pack(padx=5, pady=5)  # Display message.
    message_aos_title.pack(padx=5, pady=5, fill='both')  # Display AOS title.
    message_aos_utc_predict.pack(padx=0, pady=0)  # Display predicted AOS time in UTC.
    message_aos_predict.pack(padx=0, pady=0)  # Display predicted AOS time in local time.
    message_los_title.pack(padx=5, pady=5)  # Display AOS title.
    message_los_utc_predict.pack(padx=0, pady=0)  # Display predicted AOS time in UTC.
    message_los_predict.pack(padx=0, pady=0)  # Display predicted AOS time in local time.
    message2 = tk.Label(message,
                        text='See ARISS_Clock_readme.txt    \r'
                             'for features and information  \r'
                             'on how to use this program.   \r\r'
                             'Close this window to continue.\r',
                        font=(text_font, text_small, 'bold'),
                        fg='red')  # Message text.
    message2.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_aos_error():
    """
    Description:
      - Reports AOS error.
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
                            'AOS in incorrect format.\r'
                            'Please edit config file with\r'
                            'new AOS date/times \r '
                            'then restart ARISS_Clock.\r'
                            'Close this window to continue.\r',
                       font=(text_font, text_small, 'bold'),
                       fg='red')  # Message text.
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_los_error():
    """
    Description:
      - Reports LOS error.
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
                            'LOS in incorrect format.\r'
                            'Please edit config file with\r'
                            'new LOS date/times \r '
                            'then restart ARISS_Clock.\r'
                            'Close this window to continue.\r',
                       font=(text_font, text_small, 'bold'),
                       fg='red')  # Message text.
    message.pack(padx=5, pady=5)  # Display message.
    message.mainloop()


def report_time_check_error():
    """
    Description:
      - Reports AOS/LOS error.
      - Creates a window with an error message that LOS is before AOS.
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
                            'LOS is before AOS.\r'
                            'Please edit config file with\r'
                            'new AOS/LOS date/times \r '
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
    timer_aos_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    timer_aos.config(font=(text_font, text_large, 'bold'), width=win_width)
    timer_los_label.config(font=(text_font, text_small, 'bold'), width=win_width)
    timer_los.config(font=(text_font, text_large, 'bold'), width=win_width)
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
    current_time = current_time + 'LT  '  # Add abbreviated time zone.
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
    current_time_utc = utc_datetime.strftime(' %H:%M:%S UTC ')  # Format time per mask.
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
    current_time_school = utc_datetime.strftime(' %H:%M:%S LST ')  # Format time per mask.
    clock_school.config(text=current_time_school)  # Convert to text.
    clock_school.after(100, time_school)  # Updated every 100ms.


def time_aos():
    """
    Description:
      - AOS countdown time.
      - Uses AOS time read from config file.
      - Formats AOS time for display. Will stop at zero.
      - Updated every 100ms.

    Output:
      clock_aos

    TODO (AOS Time): None.
    """
    # Difference between current local time and AOS UTC time.
    delta = aos - time.time() - time.timezone + (time.daylight * 3600) + 1
    if delta <= yellow_alert:
        timer_aos['bg'] = aos_color_warning  # Change background color.
        timer_aos_label['bg'] = aos_color_warning  # Change background color.
    if delta <= red_alert:
        timer_aos['bg'] = aos_color_alert  # Change background color.
        timer_aos_label['bg'] = aos_color_alert  # Change background color.
    if delta >= 1:  # Update AOS time if AOS is not yet been reached.
        timer_aos['text'] = time.strftime(' %H:%M:%S AOS ', time.localtime(delta + (5 * 3600)))
    else:
        timer_aos['text'] = ' 00:00:00 AOS '  # Show zero when delta is negative.
        timer_aos['bg'] = aos_color_stopped  # Change background color when AOS is reached.
        timer_aos_label['bg'] = aos_color_stopped  # Change background color.
    timer_aos.config(font=(text_font, text_large, 'bold'))
    timer_aos.after(100, time_aos)  # Updated every 100ms.


def time_los():
    """
    Description:
      - LOS countdown time.
      - Uses LOS time read from config file.
      - Formats LOS time for display. Will stop at zero.
      - Updated every 100ms.

    Output:
      clock_los

    TODO (LOS Time): None.
    """
    delta1 = aos - time.time() - time.timezone + (time.daylight * 3600) + 1  # AOS trigger to start ET.
    delta2 = los - time.time() - time.timezone + (time.daylight * 3600) + 1  # Difference between current local time and LOS time.
    if (delta1 >= 0) & (delta2 >= 0):
        # clock_los['text'] = ' 00:00:00 LOS '  # Display before AOS.
        timer_los['text'] = '    __:__ LOS '  # Display before AOS.
        timer_los['bg'] = gray  # Change background color.
        timer_los_label['bg'] = gray  # Change background color.
    if (delta1 <= 1) & (delta2 >= 1):  # Update LOS time if LOS is not yet been reached.
        # clock_los['text'] = time.strftime('%H:%M:%S LOS', time.localtime(delta2 + (5 * 3600)))  # Shows HH:mm:ss.
        timer_los['text'] = time.strftime('    %M:%S LOS ', time.localtime(delta2 + (5 * 3600)))  # Shows only mm:ss.
        if delta2 <= red_alert:
            timer_los['bg'] = los_color_alert
            timer_los_label['bg'] = los_color_alert
        else:
            timer_los['bg'] = los_color_started  # Change background color after AOS.
            timer_los_label['bg'] = los_color_started  # Change background color after AOS.
    elif delta2 <= 1:
        # clock_los['text'] = ' 00:00:00 LOS '  # Show zero when delta is negative.
        timer_los['text'] = '    00:00 LOS '  # Show zero when delta is negative.
        timer_los['bg'] = los_color_stopped  # Change background color is LOS has occurred.
        timer_los_label['bg'] = los_color_stopped  # Change background color is LOS has occurred.
    timer_los.after(100, time_los)  # Updated every 100ms.


def time_pass_elapsed():
    """
    Description:
      - AOS elapsed time.
      - Uses AOS and LOS time read from config file.
      - Calculates and formats elapsed time for display. Start at zero.\
      - Starts when AOS is zero, stops when LOS is zero.
      - Updated every 100ms.

    Output:
      clock_pass

    TODO (Pass Times): None.
    """
    delta1 = aos - time.time() - time.timezone + (time.daylight * 3600) + 1  # AOS trigger to start ET.
    delta2 = los - time.time() - time.timezone + (time.daylight * 3600) + 1  # LOS trigger to stop ET.
    delta3 = time.time() - aos  # Calculate elapsed time since AOS.
    if delta1 >= 1:
        # clock_pass['text'] = ' 00:00:00 ET  '  # ET display before AOS.
        timer_pass_elapsed_time['text'] = '    __:__ ET  '  # ET displayed before AOS.
    elif delta2 >= 0:  # AOS trigger to start ET.
        # Shows HH:mm:ss.
        # timer_pass_elapsed_time['text'] = time.strftime(' %H:%M:%S ET  ', time.localtime(delta3 + (5 * 3600)))
        # Shows only mm:ss.
        timer_pass_elapsed_time['text'] = time.strftime('    %M:%S ET  ', time.localtime(delta3 + (5 * 3600)))
        timer_pass_elapsed_time['bg'] = pass_elapsed_time_color  # Change background color after AOS.
        timer_pass_elapsed_time_label['bg'] = pass_elapsed_time_color  # Change background color after AOS.
    timer_pass_elapsed_time.after(100, time_pass_elapsed)  # Updated every 100ms.


# ========================================================================
# MAIN
# ========================================================================

make_readme_file()  # Call the function to create readme file.
startup()  # Call the function to read and parse command line options.


# --- Read configuration data from file. ---------------------------------

# This is done one time when the script is started.
# Config file can use '#' for comments.
# ISS AOS and LOS times are in local ground station time in this exact format only:
#   AOS,YYYY-MM-DD HH:mm:ss
#   LOS,YYYY-MM-DD HH:mm:ss
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
    AOS = a_dictionary['AOS']  # Read AOS date/time.
except KeyError:
    report_aos_error()  # Call the function to report error.
    a_dictionary['AOS'] = '2021-01-01 00:00:00'  # Set default AOS
    AOS = a_dictionary['AOS']  # Read AOS date/time.
try:
    AOS = tuple([int(x) for x in AOS[:10].split('-')]) + tuple([int(x) for x in AOS[11:].split(':')])
    aos = datetime(*AOS).timestamp()  # Convert tuple.
except ValueError:
    report_aos_error()  # Call the function to report error.
    a_dictionary['AOS'] = '2021-01-01 00:00:00'  # Set default AOS
    AOS = a_dictionary['AOS']  # Read AOS date/time.
    AOS = tuple([int(x) for x in AOS[:10].split('-')]) + tuple([int(x) for x in AOS[11:].split(':')])
    aos = datetime(*AOS).timestamp()  # Convert tuple.
# aos_utc = datetime.fromtimestamp(aos, tz=timezone.utc)  # Convert local AOS time to UTC.
aos_utc = datetime.fromtimestamp(aos)
aos_utc = aos_utc.strftime('%Y-%m-%d %H:%M:%S')

# Compute AOS in local time base on UTC time in config file.
aos_local = aos - time.timezone + (time.daylight * 3600)
aos_local = datetime.fromtimestamp(aos_local)
aos_local = aos_local.strftime('%Y-%m-%d %H:%M:%S')
# print("AOS Local ", aos_local)

# --- LOS time. ----------------------------------------------------------

# Check for missing or incorrect LOS time in config file.
try:
    LOS = a_dictionary['LOS']  # Read LOS date/time.
except KeyError:
    report_aos_error()  # Call the function to report error.
    a_dictionary['LOS'] = '2021-01-01 01:00:00'  # Set default LOS
    LOS = a_dictionary['LOS']  # Read LOS date/time.
try:
    LOS = tuple([int(x) for x in LOS[:10].split('-')]) + tuple([int(x) for x in LOS[11:].split(':')])
    los = datetime(*LOS).timestamp()  # Convert tuple.
except ValueError:
    report_los_error()  # Call the function to report error.
    a_dictionary['LOS'] = '2021-01-01 01:00:00'  # Set default AOS
    LOS = a_dictionary['LOS']  # Read LOS date/time.
    LOS = tuple([int(x) for x in LOS[:10].split('-')]) + tuple([int(x) for x in LOS[11:].split(':')])
    los = datetime(*LOS).timestamp()  # Convert tuple.
# los_utc = datetime.fromtimestamp(los, tz=timezone.utc)  # Convert local LOS time to UTC.
los_utc = datetime.fromtimestamp(los)
los_utc = los_utc.strftime('%Y-%m-%d %H:%M:%S')

# Compute LOS in local time base on UTC time in config file.
los_local = los - time.timezone + (time.daylight * 3600)
los_local = datetime.fromtimestamp(los_local)
los_local = los_local.strftime('%Y-%m-%d %H:%M:%S')
# print("LOS Local ", los_local)

# --- Check that AOS is before LOS. --------------------------------------

if aos_utc > los_utc:
    report_time_check_error()  # Call the function to report AOS/LOS error message window.


# --- Report predicted AOS and LOS date/times. ---------------------------

# Show predicted AOS/LOS times to be verified in a separate window.
report_aos_los_readme()  # Call the function to report AOS and LOS predicts and readme.


# --- Debug for parameters read from config file. ------------------------

# Can comment out if it is working.
# print(a_dictionary)  # Show dictionary.
# print('STZ:', a_dictionary['STZ'])
# print(stz)
# print('AOS LOC:', a_dictionary['AOS'])
# print('AOS UTC:', aos_utc)
# print(AOS)
# print(aos)
# print('LOS LOC:', a_dictionary['LOS'])
# print('LOS UTC:', los_utc)
# print(LOS)
# print(los)


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
aos_color_warning = yellow  # Time at six minute to AOS. Warning!
aos_color_alert = red  # Time at one minute to AOS. Read alert!
aos_color_stopped = gray  # Timer stopped.
los_color_started = yellow  # Timer is running. Warning!
los_color_alert = red  # Time at one minute to LOS. Red alert!
los_color_stopped = gray  # Timer stopped.
pass_elapsed_time_color = orange  # Elapsed time after AOS.


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
                         text='ARISS ISS Contact Clock',
                         font=(text_font, text_med, 'bold'),  # Title text.
                         activebackground='white', bg=title_button_color,
                         command=report_aos_los)
# Hours, min, sec labels.
hms_label = tk.Label(root, text="hrs     min     sec           ",
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
# AOS timer.
timer_aos = tk.Label(root,
                     font=(text_font, text_large, 'bold'),
                     bg=aos_color_started,
                     padx=20)
timer_aos_label = tk.Label(root,
                           text='Countdown to Acquisition of Signal',
                           font=(text_font, text_small, 'bold'),
                           bg=aos_color_started,
                           padx=20)
# LOS timer.
timer_los = tk.Label(root,
                     font=(text_font, text_large, 'bold'),
                     bg=gray,
                     padx=20)
timer_los_label = tk.Label(root,
                           text='Countdown to Loss of Signal',
                           font=(text_font, text_small, 'bold'))
# Pass elapsed time timer.
timer_pass_elapsed_time = tk.Label(root,
                                   text='    00:00 ET  ',  # ' 00:00:00 ET  '
                                   font=(text_font, text_large, 'bold'),
                                   bg=gray,
                                   padx=20)
timer_pass_elapsed_time_label = tk.Label(root,
                                         text='ISS Pass Elapsed Time',
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
time_aos()           # Call the function to get AOS time.
time_los()           # Call the function to get LOS time.
time_pass_elapsed()  # Call the function to get pass elapsed time.


# --- Display clocks and text in window. ---------------------------------

# The order here defines the order displayed.
# Set label, then pack to display.

title_button.pack(padx=5, pady=(10, 5))  # Display title.
hms_label.pack(padx=5, pady=0)  # Display time labels.

if not display_aos_los_et_top:
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

timer_aos.pack(padx=5, pady=(10, 0))  # Display AOS countdown clock.
if display_labels:
    timer_aos_label.pack(padx=5, pady=(0, 2), fill='both')  # Display AOS title.

timer_los.pack(padx=5, pady=(10, 0))  # Display LOS countdown clock.
if display_labels:
    timer_los_label.pack(padx=5, pady=(0, 2), fill='both')  # Display AOS title.

timer_pass_elapsed_time.pack(padx=5, pady=(10, 0))  # Display pass elapsed time.
if display_labels:
    timer_pass_elapsed_time_label.pack(padx=5, pady=(0, 2))  # Display pass elapsed time.

if display_aos_los_et_top:
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
