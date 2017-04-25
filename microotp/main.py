# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License


from machine import I2C, Pin, RTC
from urtc import DS3231

bus = I2C(-1, Pin(4), Pin(5))
rtc = RTC()
rtc.datetime([x for x in DS3231(bus).datetime() if x] + [0])
del DS3231
print('Local RTC sync done')

from settings import STORAGE_FILE
from core import Core
from owner import Owner
from ssd1306 import SSD1306_I2C
from states import init
from storage import Storage
from views import Views
from wifi import WiFi

print('Modules import... done')
display = SSD1306_I2C(128, 32, bus)
print('Display initialization... done')
local_storage = Storage(STORAGE_FILE)
print('Storage initialization... done')
network = WiFi()
network.disable() # ensure wifi is off
print('Network initialized and ensured is off')
core = Core(display, network, local_storage, rtc)
owner = Owner(core, Views)

init_state = init()

def r(owner):
    owner.core.load()
    init_state.on_enter(owner)

r(owner)