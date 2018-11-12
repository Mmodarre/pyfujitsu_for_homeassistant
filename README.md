# pyfujitsu_for_homeassistant

This is a platform to support Fujitsu General Airconditioners under Climate component of Home Assistant. 

### Sample UI:

![UI_SCREENSHOT](https://github.com/Mmodarre/pyfujitsu_for_homeassistant/blob/master/Capture.PNG)
![UI_SCREENSHOT](https://github.com/Mmodarre/pyfujitsu_for_homeassistant/blob/master/Capture2.PNG)

### Usage:
1. create this directory path `/config/custom_components/climate/` if it does not already exist.

2. Download the `fujitsu_general_heatpump.py` from the repo and place it in the climate directory mentioned in previous step. So the end result would look like: `/config/custom_components/climate/fujitsu_general_heatpump.py`

3. add the below lines to your `configuration.yaml` file and replace it with your FGLair app username/password:
```
climate:
   - platform: fujitsu_general_heatpump
     username: <your FGLair username>
     password: <your FGLair password> 
```
4. Restart Home Assistant in order for the new component to show and all of your A/Cs in your account should appear in HASS.

