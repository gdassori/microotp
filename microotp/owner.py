# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from settings import OTP_SESSION
from gc import collect


class Owner:
    def __init__(self, core):
        self._state = None
        self._core = core
        self.state_at = None
        self.data_changed = False

    @property
    def ready(self):
        return bool(self._core.ready)

    @property
    def core(self):
        return self._core

    def _get_time(self):
        from gc import collect
        from utime import time
        res = time()
        del time
        collect()
        return res

    def _sleep(self, t):
        from gc import collect
        from utime import sleep
        sleep(t)
        del sleep
        collect()

    def set_state(self, state):
        if state != self._state:
            self._state and self._state.on_exit(self)
            self.state_at = self._get_time()
        self._state = state

    def ttl(self, timeout):
        t = timeout - (self._get_time() - self.state_at)
        return t > 0 and t or 0

    def bootstrap(self, timeout):
        from wifi import WiFi
        network = WiFi()
        from ssd1306 import SSD1306_I2C
        from machine import Pin, I2C
        bus = I2C(-1, Pin(4), Pin(5))
        display = SSD1306_I2C(128, 32, bus)
        from views import Views
        with network.Context(timeout) as c:
            while 1:
                ttl = self.ttl(timeout)
                if not ttl:
                    self._core.show(display, None)
                    self.data_changed = False
                    break
                self._core.show(
                    display,
                    Views['network']['wait'](c.net.token, timeout, ttl)
                )
                if c.net.connected:
                    self._core.show(
                        display,
                        Views['network']['connected']()
                    )
                    self.data_changed = self._core.setup_mode()
                    break
                self._sleep(0.5)
        del network, WiFi, display, SSD1306_I2C, Views, Pin, I2C, bus
        collect()
        return self.data_changed

    def show_current_otp(self):
        otp_tuple = self._core.get_otp_tuple()
        start = self._get_time()

        from ssd1306 import SSD1306_I2C
        from machine import Pin, I2C
        bus = I2C(-1, Pin(4), Pin(5))
        display = SSD1306_I2C(128, 32, bus)
        from views import Views
        while self._get_time() - start <= OTP_SESSION:
            self._core.show(display, Views['otp'](otp_tuple))
            self._sleep(0.5)
        del display, SSD1306_I2C, Views, Pin, I2C, bus
        collect()

    def sleep(self):
        self._core.turn_off()

