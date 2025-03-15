ARISS Clock - Change Log
========================

This record only covers official releases and not any interim development
versions.  

V3.0.0 (dev15) - 2025-03-14
---------------------------
- Fixed daylight savings time bug! Also found a way to better test
  this and verify I fixed all the places where time math was being
  done.
- Updated some terminology changing from references to "school" and 
  replaced with "event". School local time (`SLT`) is now event local 
  time (`ELT`).  School time zone (`STZ`) is now event time zone (`ETZ`).
- Added error checking for existence of logo image files.
- Improved error checking of config file.
- Added check for the desired font. Displays message window if the 
  font was substituted. This means the font was not installed per the
  README directions.
- Put UTC clock on top of local time clock to match the predict report 
  order.
- Changed the elapsed time active color to a more muted light blue.
- Cleaned out some dead code and commented out old code and test code.
- Cleaned up comments everywhere.
- Created a companion Python test script to help new Python users.
  Also helps to verify needed libraries are present.
- Dropped the Windows executable. It became too much trouble to create.
  Most virus software wants to quarantine the EXE file without a 
  certificate. Since I am not a Windows user (or Mac user), it is not 
  worth the effort for me. Users will need to install Python3 to run 
  this tool. Retained instructions on how to make a native binary for 
  those so inclined to do so.
- Updated README, HELPER, Config file, and other docs to reflect changes 
  mentioned above.

V2.0.0 (dev14) - 2024-12-12
---------------------------
- Changed terminology for AOS and LOS to Rise and Set, respectively. All  
  variables in the script were changed accordingly.
- Made a fix to correct local time calculations. This is working correctly
  for standard time. There might be (or might not) be an issue when daylight
  saving time is in effect. Time or timers could be off by one hour.
- Updated the config file terminology.
- Made some minor updates to the README file.

V1.10 (dev13) - 2024-09-04
--------------------------
- One of the `datetime` methods was being deprecated. Changed to better syntax.
  This might have been the source of some time issues a user in GB had.  
- Made things more UTC time based rather than local time based. Changed the
  AOS/LOS times in the configuration file to be UTC instead of local time.
  Had to make a number of changes to the AOS and LOS functions, initial
  AOS/LOS calculations after reading the config file, and all other places
  where time calculations were being made based on local time. Unfortunately
  the time math is now harder to follow.  
- Changed the time zone label of the local clock to `LT` for Local Time.
  Reading and displaying the local time zone abbreviation was OK. But found
  out it could be 3, 4, or even up to 5 characters. Any more than three just
  messed up the spacing. So label is fixed at 2 characters.  
- Updated the configuration file instructions. Used better wording for the
  school time zone.  
- Updated the readme file to reflect above changes.  
- For the screens that show the AOS/LOS times read from the config file,
  the UTC times are now before the local times (`LT`).  

V1.01 (dev12) - 2023-08-20
--------------------------
- Updated School Time Zone feature to account for half hour time zones
  differences. Was using an integer, and now a scalar.  

V1.00 (dev11) - 2022-03-12
--------------------------
- Baseline release.  
