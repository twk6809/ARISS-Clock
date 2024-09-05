ARISS Clock - Change Log
========================

This record only covers official releases and not any interim development
versions.  

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
