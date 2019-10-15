# Intro
A simplistic PWS (Personal Weather Station) and driver using a BME280 chip (temperature, huidity and air pressure) with the [WeeWX](http://www.weewx.com/) software.

# Background

Since it's not a full and well-known PWS setup, I followed the instructions in the [customization guide](http://www.weewx.com/docs/customizing.htm#porting) to write the driver. It's based on the [fileparser driver](https://github.com/weewx/weewx/blob/master/examples/fileparse/bin/user/fileparse.py) which is installed like [this](https://github.com/weewx/weewx/tree/master/examples/fileparse).

# Hardware

This software supports the [BME280](https://www.bosch-sensortec.com/bst/products/all_products/bme280) integrated environment sensor from Bosch for providing temperature, air pressure and humidity readings. It is assumed you have this sensor connected to an I2C bus on e.g. a Raspberry Pi. 

# Software Requirements

- A [WeeWX](http://www.weewx.com/) PWS server running on the host (e.g. a Raspberry Pi)
- The Python [RPi.BME280](https://pypi.org/project/RPi.bme280/) library to interface with the sensor

# Driver Installation

[Download](https://github.com/parautenbach/WeeWX-BME280/releases) the latest release. 

Run the following commands:
```shell
sudo wee_extension --install bme280wx.zip
sudo wee_config --reconfigure
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
```

To uninstall, just run `wee_extension --uninstall bme280wx`.

# Manual Driver Configuration

Run `i2cdetect -y 1` (where `1` is the I2C port number) from a command line to get the I2C address of the BME280 sensor.

Add the following to `/etc/weewx/weewx.conf`:

```ini
[Station]
    station_type = BME280

[BME280]
    poll_interval = 2          # number of seconds
    i2c_port = 1               # also the port number used in the comment below
    i2c_address = 0x76         # check this by running `i2cdetect -y 1` from a command-line (hex value)
```

# Credit

Thanks to the friendly [WeeWX development forum](https://groups.google.com/forum/#!searchin/weewx-development/driver%7Csort:date/weewx-development/UR_BodXOg-g/GrzwGG1GDQAJ) for pointing me in the right direction.

# Other

As a side-note, there is also this [useful extension](https://gitlab.com/wjcarpenter/bme280wx) if you have an existing PWS and would like to add additional BME280 sensors. 
