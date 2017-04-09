#
# otp.py
# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License
#
#
#  Inspired by https://github.com/pyotp/pyotp
# Copyright (C) 2011-2016 Mark Percival <m@mdp.im>,
# Nathan Reynolds <email@nreynolds.co.uk>, and PyOTP contributors

import utime
import b32dec
import hmac
import sha1


class OTP(object):
    def __init__(self, s, digits=6, digest=sha1.sha1):
        self.digits = digits
        self.digest = digest
        self.secret = s

    def generate_otp(self, input):
        if input < 0:
            raise ValueError('input must be positive integer')
        hasher = hmac.new(self.byte_secret(), self.int_to_bytestring(input), self.digest)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code
        return str_code

    def byte_secret(self):
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        return b32dec.b32decode(self.secret, casefold=True)

    @staticmethod
    def int_to_bytestring(i, padding=8):
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        res = bytes(bytearray(reversed(result)))
        return b'\0' * (padding - len(res)) + res


class TOTP(OTP):
    def __init__(self, *args, **kwargs):
        self.interval = kwargs.pop('interval', 30)
        super(TOTP, self).__init__(*args, **kwargs)

    def at(self, for_time, counter_offset=0):
        return self.generate_otp(self.timecode(for_time) + counter_offset)

    def now(self):
        return self.generate_otp(self.timecode(int(utime.time())))

    def timecode(self, for_time):
        # Epoch Y0 for embedded is 2000-01-01T00:00
        TIME_OFFSET = 946681200
        for_time += TIME_OFFSET
        print(for_time)
        return for_time // self.interval


class HOTP(OTP):
    def at(self, count):
        return self.generate_otp(count)

    def verify(self, otp, counter):
        return str(otp) == str(self.at(counter))