set -e

rm -rf build
mkdir build

mpy-cross microotp/core.py -o build/core.mpy
mpy-cross microotp/init.py -o build/init.mpy
mpy-cross microotp/otpmanager.py -o build/otpmanager.mpy
mpy-cross microotp/owner.py -o build/owner.mpy
mpy-cross microotp/settings.py -o build/settings.mpy
mpy-cross microotp/states.py -o build/states.mpy
mpy-cross microotp/storage.py -o build/storage.mpy
mpy-cross microotp/views.py -o build/views.mpy
mpy-cross microotp/wifi.py -o build/wifi.mpy
mpy-cross microotp/libs/urtc.py -o build/urtc.mpy
mpy-cross microotp/libs/ssd1306.py -o build/ssd1306.mpy
mpy-cross microotp/libs/b32dec.py -o build/b32dec.mpy
mpy-cross microotp/libs/hmac.py -o build/hmac.mpy
mpy-cross microotp/libs/sha1.py -o build/sha1.mpy
mpy-cross microotp/libs/otp.py -o build/otp.mpy
cp microotp/main.py build/

ampy -b 115200 -p /dev/ttyUSB0 put build/core.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/init.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/otpmanager.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/owner.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/settings.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/states.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/storage.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/views.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/wifi.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/urtc.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/ssd1306.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/b32dec.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/hmac.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/sha1.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/otp.mpy
ampy -b 115200 -p /dev/ttyUSB0 put build/main.py
