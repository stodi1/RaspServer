# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
import adafruit_tsl2561

class light:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.tsl = adafruit_tsl2561.TSL2561(i2c)
        self.tsl.enabled = True
        self.tsl.gain = 0
        self.tsl.integration_time = 1
        # broadband = self.tsl.broadband
        # infrared = self.tsl.infrared

    def get_data(self):
        lux = self.tsl.lux
        return [lux]