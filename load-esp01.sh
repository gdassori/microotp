set -e
ampy -p /dev/ttyUSB0 put microotp/core.py
ampy -p /dev/ttyUSB0 put microotp/main.py
ampy -p /dev/ttyUSB0 put microotp/otpmanager.py
ampy -p /dev/ttyUSB0 put microotp/owner.py
ampy -p /dev/ttyUSB0 put microotp/settings.py
ampy -p /dev/ttyUSB0 put microotp/states.py
ampy -p /dev/ttyUSB0 put microotp/storage.py
ampy -p /dev/ttyUSB0 put microotp/views.py
ampy -p /dev/ttyUSB0 put microotp/wifi.py
ampy -p /dev/ttyUSB0 put microotp/libs/urtc.py
ampy -p /dev/ttyUSB0 put microotp/libs/ssd1306.py
