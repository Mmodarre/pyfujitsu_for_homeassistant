# pyfujitsu_for_homeassistant

This is a platform to support Fujitsu General Airconditioners under Climate component of Home Assistant. The Python supporting library for accessing the FGLair API is located at: https://github.com/Mmodarre/pyfujitsu

### Sample UI:

![UI_SCREENSHOT](https://github.com/Mmodarre/pyfujitsu_for_homeassistant/blob/master/Capture.PNG)
![UI_SCREENSHOT](https://github.com/Mmodarre/pyfujitsu_for_homeassistant/blob/master/Capture2.PNG)

### Usage:
1. create this directory path `/config/custom_components/fujitsu_general_heatpump/` if it does not already exist.


2. Download the `fujitsu_general_heatpump.py` `manifest.json' and 'init.py` from the repo and place it in the  directory mentioned in previous step. Rename `fujitsu_general_heatpump.py` to `climate.py`

So the end result would look like: 
`/config/custom_components/fujitsu_general_heatpump/climate.py`
`/config/custom_components/fujitsu_general_heatpump/manifest.json`
`/config/custom_components/fujitsu_general_heatpump/init.py`

3. add the below lines to your `configuration.yaml` file and replace it with your FGLair app username/password:
```
climate:
   - platform: fujitsu_general_heatpump
     username: <your FGLair username>
     password: <your FGLair password> 
```
4. Restart Home Assistant in order for the new component to show and all of your A/Cs in your account should appear in HASS.

### Known issues and missing features:

[RESOLVED]1. Google Assistant integration is not working [most possibly due to states not matching what Google assistant is expecting]
2. Logging needs to be implemented
3. The “powerful” functionality is implemented through aux_heat button in UI
4. There are some other functionalities in the A/C which currently is not implemented.
5. Could not reverse engineer the API to give the ambient room temperature. If you figured it out let me know and I am happy to update the library.
