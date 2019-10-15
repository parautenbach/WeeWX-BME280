from weecfg.extension import ExtensionInstaller


def loader():
    return BME280Driver()


class BME280DriverInstaller(ExtensionInstaller):
    def __init__(self):
        super(BME280DriverInstaller, self).__init__(
            version="0.1.0",
            name="bme280",
            description="BME280 driver for WeeWX.",
            author="Pieter Rautenbach",
            author_email="parautenbach@gmail.com",
            config={"Station": {"station_type": "BME280"},
                    "BME280": {"poll_interval": "10",
                               "i2c_port": "1",
                               "i2c_address": "0x76",
                               "driver": "user.bme280"}},
            files=[("bin/user", ["bin/user/bme280wx.py"])]
        )
