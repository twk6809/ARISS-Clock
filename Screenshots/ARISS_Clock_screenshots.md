ARISS Clock - Screenshots
=========================
By: Ken McCaughey (N3FZX)  
On: 2025-03-14  
Ver 3.0.0   

<!-- In MarkDownd format. -->
<!-- Page breaks set for MarkText, US letter, with 10 top & bot.-->

Here are various screenshots with some explanation.


<div style="page-break-after: always;"></div>

Normal Startup
--------------

The following are 
### Greeting and Predict Check

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_greeting_predict_check.png)

Clock Operation
---------------

The following screenshots are of the ARISS Clock running with the default 
options.

### Pre-Rise

Prior to the predicted Rise time the Rise counter is active. The Set and 
Elapsed time counters are gray and show underbars.

#### Greater Than 6 Minutes

When Rise time is greater than 6 minutes the countdown to Rise is green.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_pre_rise.png)

#### Less Than 6 Minutes

When Rise time is less than 6 minutes the counter turns yellow.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_pre_rise_6m.png)

#### Less Than 1 Minute 

When Rise time is less than 1 minute the counter turns red.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_pre_rise_1m.png)

### Pre-Set

Prior to predicted Set time, the Rise time counter is gray at zero. The Set and 
Elapsed time counters are active. The Set counter will change color. The 
Elapsed time counter stay the same color.

#### Greater Than 1 Minute

While the predicted Set time is greater than one minute the counter will be
yellow.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_pre_set.png)

#### Less Than 1 Minute

When Set time is less than 1 minute the counter turns red.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_pre_set_1m.png)



Error Messages
--------------

There are a few error messages that can be encountered.

### Missing Fonts

At startup there is a check for the required fonts. If they are not found the
following window comes up. Closing this window allows the user to proceed with
a substituted font. This will result in a sloppy look and some information may
not be rendered correctly.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_error_missing_fonts.png)

### Missing Config File

If the configuration file is not found this message window will appear. A new
config file with default values will be created.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_error_config_file.png)

### RISE Time Before Set Time

This error window will appear if the Rise time in the config file is after the
Set time. The Rise/Set date/times in the config file will need to be corrected.

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_error_set_before_rise_time.png)

### RISE Time Error

The following error window will appear if the format for the Rise time is 
found in the config file. 

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_error_rise_time.png)

### Set Time Error

The following error window will appear if the format for the Set time is 
found in the config file. 

![ARISS Clock with correct font.](https://github.com/twk6809/ARISS-Clock/blob/main/Screenshots/ARISS_Clock_error_set_time.png)


Optional Looks
--------------

The look can be changed by a combination of startup switch options (see the 
README) or resizing the window.

### Black and White



### Clocks On Top



### Reduced Sizes


