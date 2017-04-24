MicroOTP - A Micropython One-Time Password Generator
====================================================

Do you use OTPs ? OTPs are good!
OTPs are a great way to protect your data from phishing and social engineering.

But what if you want to protect with a 2FA a mobile app?
Do you see yourself the roundtrip? So MicroOTP comes in handy.

Also, how precious is the data you are going to access?
Sometimes you need a place safe than a smartphone to store your One Time Passwords.
Google Authenticator is a great tool, but if you really go in paranoid mode, the smartphone is itself insecure.

Project aim is to provide a banking grade security, long-lasting, OTP generators, that easy fit in your pocket,
with schematics and everything you need to build it by yourself.

It comes with a client-side only implementation of RFC 4226 (HOTP: An HMAC-Based One-Time Password Algorithm)
and RFC 6238 (TOTP: Time-Based One-Time Password Algorithm).

Quick features overview
-----------------------

WIP

Support
-------

At this very moment the project supports:

- MicroPython 1.8.7
- Ai-Thinker ESP12
- SSD1306 I2C 128x64
- DS3231 RTC

TODO
----

- Support Apps (Mobile, Desktop, Browsers)
- Schematics
- Multiplatform build scripts
- STL Files


![microotp breadboard](https://github.com/gdassori/microotp/raw/master/docs/img/microotp-breadboard.jpg)