ARISS Clock Version 3.0.0 was written for Python 3.x on Linux.

NAME
    ARISS_Clock - Simple readable large clock to support ISS
        passes in support of ARISS event contacts at ground 
        station K6DUE.

SYNOPSIS
    Python script
        python3 ARISS_Clock.py [ -b ] [ -c ] [ -e ] [ -h ] [ -l ] [ -t ]

    Executable (if available)
        ARISS_Clock [ -b ] [ -c ] [ -e ] [ -h ] [ -l ] [ -t ]

DESCRIPTION
    ISS Rise and Set times are set in the configuration file. As the predicted
    Rise time approaches the timer changes colors. At predicted Rise time 
    the Rise timer stops at zero and the Set and Elapse Time (ET) timers 
    start. The Set timer changes colors as predicted Set time is approached.
    At the predicted Set time the Set timer and ET timers stop.

    There are several clocks that are displayed. The UTC clock is displayed
    first followed by the Local Time (LT) zone. Time zone is detected for the 
    local time clock. Finally, there is an optional event local time (ELT) clock. 
    The Event Time Zone (ETZ) UTC time zone offset is specified in the config 
    file. This clock label is fixed as Event Local Time (ELT).

COMMAND LINE OPTIONS
    -b, -B, --BW
        Force Rise/Set timers to use only black & white colors.
        Default is to use color for active timers.

    -c, -C, --Color
        Force background colors off.
        Default is color.

    -e, -E, --Event
        Turn OFF display Event Local Time (ELT) clock.
        Default is to display the clock.

    -h, -H, --Help
        Lists the command line options in terminal window, then exits.
        This will override all other command line options.

    -l, -L, --Labels
        Turn OFF the display of the timer and clock labels.
        Default is to display the labels.

    -t, -T, --Top
        Remove timers from the top of the display and move to bottom.
        Default is to have timers at the top and clocks on bottom.

    If any option is invalid the program uses all the defaults.

EXAMPLES
    python3 ARISS_Clock.py or python3 ARISS_Clock.py
        Run the script from python using look and feel defaults.

    python3 ARISS_Clock.py -l
        Run the script from python with labels not displayed.

    python3 ARISS_Clock.py -T
        Run the script from python with the timers to the bottom of
        the display.

    python3 ARISS_Clock.py --BW
        Run the script from python with black & white timers, no colors.

    python3 ARISS_Clock.py -l -t -b
        Run the script from python with all command line options. Order
        does not matter. Can be upper and lower case. See above.

OVERVIEW
    Predicted Rise and Set times can be viewed in a separate window by
    clicking on the "ARISS Contact Clock" button. Rise and Set predicted
    date/times are displayed in local and UTC. These should be verified
    against the satellite tracking software. Edit the config file if
    incorrect and restart the ARISS Clock.

    The Rise countdown timer only shows the hours, minutes, and seconds.
    If Rise is more than 24 hours away, the Rise will get to zero and
    roll over. If Rise and Set have already passed when the script is
    started, the Rise, Set, and ET timers will all show zero. The timers
    change color over time as Rise and Set are reached, unless the -b
    command line option was used.

    Timer colors change based on the time matching the config file
    Rise and Set times.

    Rise and Set timer colors change as follows:
        Rise timer starts off GREEN when active.
        Set and ET timers start off grayed out while Rise is not zero.
        Rise timer goes YELLOW at less than 6 minutes to go. Warning!
        Rise timer goes RED at less than 1 minute(s) to go. Red alert!
        Rise timer goes GRAY at zero. The contact has started.
        Set timer starts off YELLOW when active. Contact in progress.
        ET timer turns blue when is becomes active.
        Set timer goes RED at less than 1 to go. Red alert!
        Set timer goes GRAY at zero when Set is reached. Contact has ended.

    Clock window can be resized. Fonts are scaled based on window width.
    To shrink, recommend adjusting the width first, then the height.
    To enlarge, recommend adjusting the height first, then the width.

    Clocks or timers at the bottom of the display can be rolled up and 
    hidden from view. Grab the bottom the window and drag up. Expand the
    window to expose.

    Rise time is checked to make sure it is before the Set time. If not,
    an error message comes up. For setting the Rise and Set times, the
    date matters. The Rise and Set timers will not change unless the date
    and time matches the UTC time clock. UTC is calculated based on the 
    system's time zone information read from the operating system.

FONTS
    This script tries to use the "DejaVu Sans Mono" non-proportional
    font. Not all systems may have this font. If the specified font is
    not found it gets substituted with a different font and this will
    affect the look and feel. It is strongly recommend to install the 
    correct fonts. The fonts are free. See INTERNET RESOURCES below.

    Required font files:
        DejaVuSansMono.ttf
        DejaVuSansMono-Bold.ttf

FILES AND DIRECTORIES
    All the files should be in the same folder.

    ARISS_Clock.py
        Python script. Main program. Requires python 3.x to run.
        Requires a number of Python libraries that may not be included
        with Python by default. Use pip to install.

    ARISS_Clock_config.txt
        The Rise and Set times and event time zone are set in the
        configuration file. Instructions are included in the file. At
        startup the configuration file is read. If the config file is
        not found in the same folder as the program,a new config file
        is created and the Rise and Set times will need to be updated.

        Verify configuration file version matches the ARISS Clock version.
        If not, delete the configuration file and restart. A new file will
        be generated with default values Edit for new event time zone 
        offset, Rise and Set date/times.

        If the configuration file gets corrupted, just delete it, and
        restart the ARISS Clock. A new file will be created.

    ARISS_Clock_readme.txt
        This help file. The file is generated every time the program is
        started up.

    ARISS_logo.png
        ARISS logo image used by the python script. Must be present if
        running the .py file.

    ARISS_logo_simple.ico
        ARISS logo icon image. Used by Windows.

AUTHOR
    By Ken McCaughey (N3FZX) for the K6DUE ARISS ground station.
    Copyright 2025.

INTERNET RESOURCES
   DejaVu Fonts at https://dejavu-fonts.github.io or from
   1001 Fonts at https://www.1001fonts.com/dejavu-sans-mono-font.html

