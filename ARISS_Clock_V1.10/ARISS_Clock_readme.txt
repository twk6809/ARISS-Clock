ARISS Clock Version 1.10 was written for Python 3.x on Linux.

NAME
    ARISS_Clock - Simple readable large clock to support ISS
        passes in support of ARISS school contacts at ground 
        station K6DUE.

SYNOPSIS
    Executable
        ARISS_Clock [ -b ] [ -c ] [ -h ] [ -l ] [ -s ] [ -t ]

    Python script
        python ARISS_Clock.py [ -b ] [ -c ] [ -h ] [ -l ] [ -s ] [ -t ]

DESCRIPTION
    AOS and LOS times are set in the configuration file. As the AOS
    approaches the timer changes colors. At AOS the AOS timer stops
    at zero and the LOS and ET timers start. The LOS timer changes
    colors as LOS is approached. At LOS the LOS timer and ET timers
    stop.

    There are several clocks that are displayed. The local time zone
    is detected for the local time clock. A UTC clock is displayed next.
    Finally, there is a optional local school time clock. The School Time
    Zone (STZ) UTC time zone offset is specified in the config file. This
    clock label is fixed as Local School Time (LST).

COMMAND LINE OPTIONS
    -b, -B, --BW
        Force AOS/LOS timers to use only black & white colors.
        Default is to use color for active timers.

    -c, -C, --Color
        Force background colors off.
        Default is color.

    -h, -H, --Help
        Lists the command line options in terminal window, then exits.
        This will override all other command line options.

    -l, -L, --Labels
        Turn OFF the display of the timer and clock labels.
        Default is to display the labels.

    -s, -S, --School
        Turn OFF display Local School Time (LST) clock.
        Default is to display the clock.

    -t, -T, --Top
        Remove clocks from the top of the display and move to bottom.
        Default is to have them at the top.

    If any option is invalid the program uses all the defaults.

EXAMPLES
    python ARISS_Clock.py or python3 ARISS_Clock.py
        Run the script from python using look and feel defaults.

    python ARISS_Clock.py -l
        Run the script from python with labels not displayed.

    python ARISS_Clock.py -T
        Run the script from python with the clocks to the bottom of
        the display.

    python ARISS_Clock.py --BW
        Run the script from python with black & white timers, no colors.

    python ARISS_Clock.py -l -t -b
        Run the script from python with all command line options. Order
        does not matter. Can be upper and lower case. See above.

    ARISS_Clock -l -t -b
        Run the executable with all command line options. The executable
        can use all the command line options that same way as the python
        script. A native executable not available for all operating systems.

OVERVIEW
    Predicted AOS and LOS can be viewed in a separate window by
    clicking on the "ARISS ISS Contact Clock" button. AOS and LOS 
    predicted date/times are displayed in local and UTC. These should be
    verified against the satellite tracking software. Edit the config file
    if incorrect and restart the ARISS Clock.

    The AOS countdown timer only shows the hours, minutes, and seconds.
    If AOS is more than 24 hours away, the AOS will get to zero and
    roll over. If AOS and LOS have already passed when the script is
    started, the AOS, LOS, and ET timers will all show zero. The timers
    change color over time as AOS and LOS are reached, unless the -b
    command line option was used.

    Timer colors change based on the time matching the config file
    AOS and LOS times.

    AOS and LOS timer colors change as follows:
        AOS starts off GREEN when active.
        LOS and ET start off grayed out while AOS is not zero.
        AOS goes YELLOW at less than 6 minutes to go. Warning!
        AOS goes RED at less than 1 minute(s) to go. Red alert!
        AOS goes GRAY at zero. The contact has started.
        LOS starts off YELLOW when active. Contact in progress.
        LOS goes RED at less than 1 to go. Red alert!
        LOS goes GRAY at zero when LOS is reached. Contact has ended.

    Clock window can be resized. Fonts are scaled based on window width.
    To shrink, recommend adjusting the width first, then the height.
    To enlarge, recommend adjusting the height first, then the width.

    Clocks or timers at the bottom of the display can be rolled up and 
    hidden from view. Grab the bottom the window and drag up. Expand the
    window to expose.

    AOS is checked to make sure it is before the LOS time. If not, an
    error message comes up. For setting the AOS and LOS times, the date
    matters. The AOS and LOS timers will not change unless the date and
    time matches the UTC time clock. UTC is calculated based on the     
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

    ARISS_Clock.exe (may not be included)
        Windows executable version of main program.

    ARISS_Clock_config.txt
        The AOS and LOS times and school time zone are set in the
        configuration file. Instructions are included in the file. At
        startup the configuration file is read. If the config file is
        not found in the same folder as the program,a new config file
        is created and the AOS and LOS times will need to be updated.

        Verify configuration file version matches the ARISS Clock version.
        If not, delete the configuration file and restart. A new file will
        be generated with default values Edit for new school time zone 
        offset, AOS and LOS date/times.

        If the configuration file gets corrupted, just delete it, and
        restart the ARISS Clock. A new file will be created.

    ARISS_Clock_readme.txt
        This help file. The file is generated every time the program is
        started up.

    ARISS_logo.png
        ARISS logo image used by the python script. Must be present if
        running the .py file. Built into the executable.

    ARISS_logo_simple.ico
        ARISS logo icon image. Used by Windows.

    ARISS_Clock.spec (may not be included)
        File with preset parameters to create an executable version
        using "pyinstaller". Syntax is "pyinstaller ARISS_Clock.spec'.

AUTHOR
    By Ken McCaughey (N3FZX) for the K6DUE ARISS ground station.

INTERNET RESOURCES
   DejaVu Fonts at https://dejavu-fonts.github.io or from
   1001 Fonts at https://www.1001fonts.com/dejavu-sans-mono-font.html

