# DFRobot Unihiker Scale

[Unihiker](https://www.unihiker.com/) is a neat touchscreen capable single board computer from [DFRobot](https://www.dfrobot.com/). The Unihiker runs a customized version of Debian and provides a "Pinpong" library to interface with the various GPIO.

For this project I'll be controlling an LED ring, interfacing with the onboard buttons and light sensor, and using i2c to communicate with a [HX711 pressure sensor kit from DFRobot](https://wiki.dfrobot.com/HX711_Weight_Sensor_Kit_SKU_KIT0176).

---------

This project contains two different connections that need to be made. The first connection is to one of the board's i2c ports. The DFRobot Gravity HX711 pressure sensor kit uses the same pinout for i2c as the Unihiker (one would expect given they are both DFRobot products) so both the same pinout and connector are in use which makes for an easy connection.

For the LED ring you can optionally ignore it if you don't want a night more or pick up a cheap aliexpress 8 LED ring. I soldered a JST connector to the back of mine so I could more easily connect to the Unihiker via its provided cord. I have that plugged into port 22 which you can determine by looking at the Unihiker silkscreen near the connectors where a number will be highlighted for each sensor connector.

## Install
For the purposes of demonstrating the script I've included the library for accessing the hx711 over i2c at the same level (I support I could have placed it alongside all the DFRobot libraries).

As such I suggest for install just placing these at the root or wherever you want to then access via the run programs feature of Unihiker.

## Customization

You can customize the script by changing the associated ENV variables.

```
CALIBRATION_WEIGHT_VALUE=50
LIGHT_ENABLE_THRESHOLD = 300
```

The former is the weight in grams that the scale expects a calibration weight to be provided with. I only had a 50g weight so opted to use that.

The latter is the sensor value at which the LEDs will enable if it drops below this threshold. It's arbitrarily set based on what I noticed to work well for my room.
