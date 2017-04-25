# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from core import Core
from owner import Owner
print('Modules import... done')

core = Core()
owner = Owner(core)


def run(owner):
    from utime import sleep
    sleep(0.1)
    from gc import collect
    from machine import I2C, Pin, RTC
    bus = I2C(-1, Pin(4), Pin(5))
    from urtc import DS3231
    rtc = RTC()
    dl = [x for x in DS3231(bus).datetime() if x]
    rtc.datetime(dl + [0 for x in range(0, 8 - len(dl))])
    del I2C, Pin, DS3231, rtc, dl
    collect()
    print('Local RTC sync done')
    sleep(0.2)
    from network import WLAN, AP_IF
    WLAN(AP_IF).active(False)
    del WLAN, AP_IF
    collect()
    print('Network initialized and ensured as off')
    sleep(0.2)
    from gc import collect
    from states import init
    init_state = init()
    owner.core.load()
    collect()
    init_state.on_enter(owner)