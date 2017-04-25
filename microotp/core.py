# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License


from views import DATETIME_LINE
from settings import DEEPSLEEP
from gc import collect as gcc
from micropython import mem_info


class Core():
    def __init__(self):
        self._last_view = dict()
        self._current_otp = 0
        self.jsondata = None
        self._cached_otp = {}

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
        from utime import time
        _now = time()
        if not self._cached_otp or self._cached_otp['e'] < _now:
            data = self._get_otp_tuple()
            self._cached_otp = {
                'd': data,
                'e': _now + (30 - (_now % 30))
            }
        ttl = self._cached_otp['e'] - _now
        otp_tuple = (self._cached_otp['d'][0], self._cached_otp['d'][1], ttl)
        del time
        gcc()
        print(otp_tuple)
        return otp_tuple

    def _get_otp_tuple(self):
        if not self.jsondata:
            raise ValueError()
        from otpmanager import OTPManager as OTPM
        from utime import sleep
        otpdata = self.jsondata['otp']['rows'][self._current_otp]
        otp = OTPM(otpdata)
        code = otp.get_code()
        sleep(0.1)
        otptuple = (otpdata['alias'], code, otpdata['frame'])
        del otp, OTPM, sleep
        gcc()
        return otptuple

    def show(self, display, view):
        display.fill(0)
        if view:
            from views import get_datestring
            coords = dict(line0=(0,0), line1=(0,12), line2=(0, 24), line2b=(64,24))
            for line in view:
                display.text(view[line], coords[line][0], coords[line][1])
            if DATETIME_LINE not in view:
                display.text(get_datestring(), coords[DATETIME_LINE][0], coords[DATETIME_LINE][1])
            del get_datestring, coords
            gcc()
        self._last_view = view
        display.show()
        print(mem_info())

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