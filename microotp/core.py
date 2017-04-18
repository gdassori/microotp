# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

import os
import machine
from settings import DEEPSLEEP
from otpmanager import OTPManager


class Core():
    def __init__(self, display, network, storage_manager, rtc, keypad=None):
        self._display = display
        self._network = network
        self._storage_manager = storage_manager
        self._keypad = keypad
        self._last_view = dict()
        self._last_otp = 0
        self._rtc = rtc
        self._otp_storage = None
        self.otp = None

    def load(self):
        self._storage = self._storage_manager.get_or_create()
        print('Loaded storage: {}'.format(self._storage))
        if self._storage.get('otp'):
            self.load_otp()
        return self

    def load_otp(self):
        try:
            self._last_otp = int(chr(self._rtc.memory(1)))
        except ValueError:
            self._last_otp = 0
        self.otp = OTPManager(self._storage['otp']['rows'], int(self._last_otp))

    def get_network_token(self):
        r = str(int.from_bytes(os.urandom(2), 'little'))
        t = '0' * (4 - len(r)) + r
        return t[:4]

    def load_next_otp(self):
        self.otp = self.otp.next_otp()
        self._rtc.memory(1, str(self.otp.pos))

    def _format_datetime(self, datetime):
        return "{}-{}-{} {}:{}:{}".format(str(datetime[0])[2:],
                                          datetime[1],
                                          datetime[2],
                                          datetime[4],
                                          datetime[5],
                                          datetime[6])
    def show(self, view):
        self._display.fill(0)
        if view:
            coords = dict(line0=(0,0), line1=(0,12), line2=(0, 24), line2b=(64,24))
            for line in view:
                if not self._last_view or self._last_view.get(line) != view[line]:
                    print('Show text ( {} ) on line ( {} )'.format(view[line], coords[line]))
                self._display.text(view[line], coords[line][0], coords[line][1])
            datestring = self._format_datetime(
                self._rtc and self._rtc.datetime(),
            )
            if 'line0' not in view:
                self._display.text(datestring, coords['line0'][0], coords['line0'][01])
        self._last_view = view
        self._display.show()

    def get_network(self, token, timeout=None):
        return self._network.Context(token, timeout)

    def setup_mode(self):
        return True

    def turn_off(self):
        self._display.poweroff()
        if DEEPSLEEP:
            print('Going into deepsleep')
            machine.deepsleep()