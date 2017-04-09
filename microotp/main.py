# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

#import sys
#sys.path.insert('./libs', 0)

from settings import BUILD, STORAGE_FILE
from machine import I2C, Pin
from core import Core
from owner import Owner
from ssd1306 import SSD1306_I2C
from states import init
from storage import Storage
from views import Views
from wifi import WiFi




bus = I2C(-1, Pin(2), Pin(0))
display = SSD1306_I2C(128, 32, bus)

local_storage = Storage(STORAGE_FILE)
network = WiFi()
network.disable() # ensure wifi is off
core = Core(display, network, local_storage)
owner = Owner(core, Views)

init_state = init()

def r(owner):
    owner.core.load()
    if BUILD is 'ESP01' and owner.ready:
        # No suppl IO available - OTP rotation
        core.load_next_otp()

    init_state.on_enter(owner)

r(owner)