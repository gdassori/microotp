# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from settings import STORAGE_FILE
from machine import I2C, Pin
from core import Core
from owner import Owner
from ssd1306 import SSD1306_I2C
from states import init
from storage import Storage
from views import Views
from wifi import WiFi
from urtc import DS3231


bus = I2C(-1, Pin(4), Pin(5))
display = SSD1306_I2C(128, 32, bus)
rtc = DS3231(bus)

local_storage = Storage(STORAGE_FILE)
network = WiFi()
network.disable() # ensure wifi is off
core = Core(display, network, local_storage, rtc)
owner = Owner(core, Views)

init_state = init()

def r(owner):
    owner.core.load()
    init_state.on_enter(owner)

r(owner)