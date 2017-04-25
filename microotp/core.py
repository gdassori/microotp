# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License


from views import DATETIME_LINE
from settings import DEEPSLEEP
from gc import collect as gcc
from micropython import mem_info # DEBUG MODE


class Core():
    def __init__(self):
        self._last_view = dict()
        self._current_otp = 0
        self.jsondata = None

    @property
    def ready(self):
        return bool(self.jsondata)

    def load(self):
        from storage import Storage as S
        from settings import STORAGE_FILE
        self.jsondata = S(STORAGE_FILE).get_or_create()
        del S, STORAGE_FILE
        gcc()
        return self

    def get_otp_tuple(self):
        if not self.jsondata:
            raise ValueError()
        print('aaaa ', mem_info())
        from otpmanager import OTPManager as OTPM
        print('bbbb ', mem_info())
        otp = OTPM(self.jsondata['otp']['rows'][self._current_otp])
        print('cccc', mem_info())
        otptuple = (
            otp.get_alias(),
            otp.get_code(),
            otp.get_ttl()
        )
        print('dddd', mem_info())
        del otp, OTPM
        print('eeee', mem_info())
        gcc()
        print('ffff', mem_info())
        return otptuple

    def show(self, display, view):
        display.fill(0)
        if view:
            from views import get_datestring as gds
            coords = dict(line0=(0,0), line1=(0,12), line2=(0, 24), line2b=(64,24))
            for line in view:
                display.text(view[line], coords[line][0], coords[line][1])
            datestring = gds()
            if DATETIME_LINE not in view:
                display.text(datestring, coords[DATETIME_LINE][0], coords[DATETIME_LINE][1])
            del gds, coords, datestring
            gcc()
        self._last_view = view
        display.show()

    def setup_mode(self):
        return True

    def turn_off(self):
        from ssd1306 import SSD1306_I2C
        from machine import I2C, Pin
        display = SSD1306_I2C(128, 32, I2C(-1, Pin(4), Pin(5)))
        display.poweroff()
        from machine import deepsleep
        if DEEPSLEEP:
            deepsleep()