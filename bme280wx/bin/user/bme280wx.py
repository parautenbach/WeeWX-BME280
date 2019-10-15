#!/usr/bin/python
#
# A WeeWX driver that reads data from a BME280 sensor attached to a Raspberry Pi. 
#
# Derived from https://github.com/weewx/weewx/blob/master/examples/fileparse/bin/user/fileparse.py.
#
# More details on the sensor:
#     o https://learn.sparkfun.com/tutorials/sparkfun-bme280-breakout-hookup-guide/all
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.
#
# See http://www.gnu.org/licenses/

# Software dependencies:
#     o https://pypi.org/project/RPi.bme280/
#
# To use this driver, put this file in the weewx user directory, then make
# the following changes to weewx.conf:
#
# [Station]
#     station_type = BME280
#
# [BME280]
#     poll_interval = 2          # number of seconds
#     i2c_port = 1               # also the port number used in the comment below
#     i2c_address = 0x76         # check this by running `i2cdetect -y 1` from a command-line (hex value)

import syslog
import time

import weewx.drivers
import smbus2
import bme280

DRIVER_NAME = "BME280"
DRIVER_VERSION = "0.1.0"


def log_debug(message):
    logmsg(syslog.LOG_DEBUG, message)

def log_info(message):
    logmsg(syslog.LOG_INFO, message)

def log_error(message):
    logmsg(syslog.LOG_ERR, message)

def loader(config_dict, engine):
    return FileParseDriver(**config_dict[DRIVER_NAME])


class BME280Driver(weewx.drivers.AbstractDevice):
    """A WeeWX driver that reads data from a BME280 sensor attached to a Raspberry Pi."""

    def __init__(self, **station_dict):
        # default is 10s
        self._poll_interval = float(station_dict.get("poll_interval", 10))
        # default is 1; specified in base 10
        self._i2c_port = int(station_dict.get("i2c_port", 1))
        # default is 0x76; specified in base 16 (hex)
        self._i2c_address = int(station_dict.get("i2c_address", 0x76), 16)

        log_info("Polling interval: {:.2f}}".format(self._poll_interval))
        log_info("I2C port: {}}".format(self._i2c_port))
        log_info("I2C address: {:0#x}".format(self._i2c_address))

        self._bus = smbus2.SMBus(port)
        self._calibration_params = bme280.load_calibration_params(self._bus, self._i2c_address)

    def genLoopPackets(self):
        while True:
            data = {}
            try:
                data = bme280.sample(self._bus, self._i2c_address, self._calibration_params)

                # https://github.com/weewx/weewx/blob/master/bin/schemas/wview.py
                # https://github.com/weewx/weewx/blob/master/bin/weewx/units.py
                packet = {"dateTime": int(time.time()),
                          "usUnits": weewx.METRIC}
                # use?
                # print(data.id)
                # print(data.timestamp)
                # cast?
                packet["outTemp"] = float(data.temperature)
                packet["pressure"] = float(data.pressure)
                packet["outHumidity"] = float(data.humidity)

                yield packet

            except Exception as e:
                log_error(e)
            finally:
                time.sleep(self._poll_interval)

    @property
    def hardware_name(self):
        return DRIVER_NAME

# To test this driver, run it directly as follows:
#   PYTHONPATH=/home/weewx/bin python ./bme280.py
if __name__ == "__main__":
    import weeutil.weeutil
    driver = BME280Driver()
    for packet in driver.genLoopPackets():
        print(weeutil.weeutil.timestamp_to_string(packet["dateTime"]), packet)