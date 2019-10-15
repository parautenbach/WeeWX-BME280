from weecfg.extension import ExtensionInstaller


def loader():
    return BME280WXDriverInstaller()


class BME280WXDriverInstaller(ExtensionInstaller):
    def __init__(self):
        super(BME280WXDriverInstaller, self).__init__(
            version="0.1.0",
            name="BME280WX",
            description="BME280 driver for WeeWX.",
            author="Pieter Rautenbach",
            author_email="parautenbach@gmail.com",
            config={"Station": {"station_type": "BME280WX"},
                    "BME280WX": {"poll_interval": "10",
                                 "i2c_port": "1",
                                 "i2c_address": "0x76",
                                 "driver": "user.bme280wx"}},
            files=[("bin/user", ["bin/user/bme280wx.py"])]
        )
