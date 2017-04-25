set -e
ampy -b 115200 -p /dev/ttyUSB0 put microotp/core.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/main.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/otpmanager.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/owner.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/settings.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/states.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/storage.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/views.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/wifi.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/urtc.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/ssd1306.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/b32dec.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/hmac.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/sha1.py
ampy -b 115200 -p /dev/ttyUSB0 put microotp/libs/otp.py
