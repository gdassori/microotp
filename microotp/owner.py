# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

import utime
from settings import OTP_SESSION


class Owner:
    def __init__(self, core, views):
        self._state = None
        self._core = core
        self._views = views
        self.state_at = None
        self.data_changed = False

    @property
    def ready(self):
        return bool(self._core.otp)

    @property
    def has_input(self):
        return self._core.keypad and self._core.command

    @property
    def core(self):
        return self._core

    def set_state(self, state):
        if state != self._state:
            self._state and self._state.on_exit(self)
        self.state_at = utime.time()
        self._state = state

    def ttl(self, timeout):
        t = timeout - (utime.time() - self.state_at)
        return t > 0 and t or 0

    def bootstrap(self, timeout):
        context = self._core.get_network(
            self._core.get_network_token()
        )
        with context as c:
            while 1:
                ttl = self.ttl(timeout)
                if not ttl:
                    self._core.show(None)
                    return False
                self._core.show(
                    self._views['network']['wait'](c.net.token, timeout, ttl)
                )
                if c.net.connected:
                    self._core.show(
                        self._views['network']['connected']()
                    )
                    self.data_changed = self._core.setup_mode()
                    return self.data_changed
                utime.sleep(0.5)

    def show_current_otp(self):
        start = utime.time()
        while utime.time() - start <= OTP_SESSION:
            self._core.show(
                self._views['otp'](self._core.otp)
            )
            utime.sleep(0.5)

    def sleep(self):
        self._core.turn_off()

