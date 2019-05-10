"""
Support for the Fujitsu General Split A/C Wifi platform AKA FGLair .

"""

import logging
import voluptuous as vol

from homeassistant.components.climate import (
    PLATFORM_SCHEMA,
    ClimateDevice
)

from homeassistant.components.climate.const import (
    ATTR_AWAY_MODE, ATTR_CURRENT_TEMPERATURE, ATTR_FAN_MODE,
    ATTR_OPERATION_MODE, ATTR_SWING_MODE, STATE_AUTO, STATE_COOL, STATE_DRY,
    STATE_FAN_ONLY, STATE_HEAT, SUPPORT_AWAY_MODE, SUPPORT_FAN_MODE,
    SUPPORT_ON_OFF, SUPPORT_OPERATION_MODE, SUPPORT_SWING_MODE,
    SUPPORT_TARGET_TEMPERATURE,  SUPPORT_AUX_HEAT
)

from homeassistant.const import (ATTR_TEMPERATURE, CONF_USERNAME, CONF_PASSWORD, TEMP_CELSIUS,STATE_ON, STATE_OFF,STATE_ON)
import homeassistant.helpers.config_validation as cv

REQUIREMENTS = ['pyfujitsu==0.8.1.1']


_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})

HA_STATE_TO_FUJITSU = {
    STATE_FAN_ONLY: 'Fan',
    STATE_DRY: 'Dry',
    STATE_COOL: 'Cool',
    STATE_HEAT: 'Heat',
    STATE_AUTO: 'Auto',
    STATE_OFF: 'Off',
    STATE_ON: 'On'
}

FUJITSU_TO_HA_STATE = {
    'Fan': STATE_FAN_ONLY,
    'Dry': STATE_DRY,
    'Cool': STATE_COOL,
    'Heat': STATE_HEAT,
    'Auto': STATE_AUTO,
    'fan': STATE_FAN_ONLY,
    'dry': STATE_DRY,
    'cool': STATE_COOL,
    'heat': STATE_HEAT,
    'Auto': STATE_AUTO,
    
    'Off': STATE_OFF,
    'off': STATE_OFF,
    
    'On': STATE_ON,
    'on': STATE_ON
}

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Fujitsu Split platform."""
    import pyfujitsu.api as fgapi
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    _LOGGER.debug("Added Fujitsu Account for username: %s ", username)
    
    fglairapi = fgapi.Api(username, password)
    if not fglairapi._authenticate():
        _LOGGER.error("Unable to authenticate with Fujistsu General")
        return

    devices = fglairapi.get_devices_dsn()
    add_entities(FujitsuClimate(fglairapi, dsn) for dsn in devices)

class FujitsuClimate(ClimateDevice):
    """Representation of a Fujitsu Heatpump."""

    def __init__(self, api, dsn):
        #from homeassistant.components.pyfujitsu import splitAC
        from pyfujitsu import splitAC
        self._api = api
        self._dsn = dsn
        self._fujitsu_device = splitAC.splitAC(self._dsn, self._api)
        self._name = self.name
        self._aux_heat = self.is_aux_heat_on
        self._target_temperature = self.target_temperature
        self._unit_of_measurement = self.unit_of_measurement
        self._current_fan_mode = self.current_fan_mode
        self._current_operation = FUJITSU_TO_HA_STATE[self.current_operation]
        self._current_swing_mode = self.current_swing_mode
        self._fan_list = ['Quiet', 'Low', 'Medium', 'High', 'Auto']
        self._operation_list = [FUJITSU_TO_HA_STATE['Heat'], FUJITSU_TO_HA_STATE['Cool'], FUJITSU_TO_HA_STATE['Auto'], FUJITSU_TO_HA_STATE['Dry'], FUJITSU_TO_HA_STATE['Fan'],FUJITSU_TO_HA_STATE['Off'],FUJITSU_TO_HA_STATE['On']]
        self._swing_list = ['Vertical Swing','Horizontal Swing', 'Vertical high',
                            'Vertical Mid', 'Vertical Low' ]
        self._target_temperature_high = self.target_temperature_high
        self._target_temperature_low = self.target_temperature_low
        self._on = self.is_on
        self._supported_features = SUPPORT_TARGET_TEMPERATURE \
            | SUPPORT_OPERATION_MODE | SUPPORT_FAN_MODE  \
            | SUPPORT_SWING_MODE | SUPPORT_ON_OFF | SUPPORT_AUX_HEAT

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._fujitsu_device.device_name['value']


    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_CELSIUS


    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return FUJITSU_TO_HA_STATE[self._fujitsu_device.operation_mode_desc]

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._fujitsu_device.adjust_temperature_degree

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return 0.5

    @property
    def powerfull_mode(self):
        """ Return Powerfull mode state"""
        return self._fujitsu_device.powerful_mode


    @property
    def is_on(self):
        """Return true if on."""
        if self._fujitsu_device.operation_mode['value'] != 0:
            return True
        else:
            return False

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        return self._fujitsu_device.get_fan_speed_desc()

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        return self._fan_list

    @property
    ## Todo combine swing modes in to one
    def current_swing_mode(self):
        """Return the fan setting."""
        return self._fujitsu_device.af_horizontal_direction['value']

    @property
    def swing_list(self):
        """Return the list of available swing modes."""
        return self._swing_list

    def set_temperature(self, **kwargs):
        """Set new target temperature."""
        self._fujitsu_device.changeTemperature(kwargs.get(ATTR_TEMPERATURE))

    def set_fan_mode(self, fan_mode):
        """Set new target fan mode."""
        print(fan_mode)
        self._fujitsu_device.changeFanSpeed(fan_mode)

    def set_operation_mode(self, operation_mode):
        """Set new target operation mode."""
        self._fujitsu_device.changeOperationMode(operation_mode)

#    def set_swing_mode(self, swing_mode):
#        """Set new target swing operation."""
#        raise NotImplementedError()

    def turn_on(self):
        """Turn device on."""
        return self._fujitsu_device.turnOn()


    def turn_off(self):
        """Turn device off."""
        return self._fujitsu_device.turnOff()

    @property
    def is_aux_heat_on(self):
        """Reusing is for Powerfull mode."""
        if self._fujitsu_device.powerful_mode['value'] == 1:
            return True
        else:
            return False

    def turn_aux_heat_on(self):
        """Reusing is for Powerfull mode."""
        self._fujitsu_device.powerfull_mode_on()

    def turn_aux_heat_off(self):
        """Reusing is for Powerfull mode."""
        self._fujitsu_device.powerfull_mode_off()

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features

    def update(self):
        """Retrieve latest state."""
        self._fujitsu_device.refresh_properties()
