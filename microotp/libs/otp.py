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


from gc import collect
from micropython import mem_info


class OTP(object):
    def __init__(self, s, digits=6):
        self.digits = digits
        self.secret = s

    def generate_otp(self, input):

        bs = self.byte_secret()
        if input < 0:
            raise ValueError('input must be positive integer')
        from hmac import new
        from sha1 import sha1
        _bytestring = self.int_to_bytestring(input)
        hasher = new(bs, _bytestring, sha1)
        del sha1, new, bs, _bytestring
        collect()
        digest = hasher.digest()
        from ubinascii import hexlify
        hexdigest = hexlify(digest)
        del hexlify, hasher
        collect()
        hmac_hash = bytearray(hexdigest)
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code
        del code, offset, hmac_hash
        collect()
        return str_code

    def byte_secret(self):
        from b32dec import b32decode
        missing_padding = len(self.secret) % 8
        if missing_padding != 0:
            self.secret += '=' * (8 - missing_padding)
        res = b32decode(self.secret, casefold=True)
        del b32decode, missing_padding
        collect()
        return res

    @staticmethod
    def int_to_bytestring(i, padding=8):
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        _bytearray = bytes(bytearray(reversed(result)))
        res = b'\0' * (padding - len(_bytearray)) + _bytearray
        del result, _bytearray
        return res


class TOTP(OTP):
    def __init__(self, *args, **kwargs):
        self.interval = kwargs.pop('interval', 30)
        super(TOTP, self).__init__(*args, **kwargs)

    def now(self):
        from utime import time
        _now = self.timecode(int(time()))
        del time
        collect()
        res = self.generate_otp(_now)
        del _now
        collect()
        return res

    def timecode(self, for_time):
        # Epoch Y0 for embedded is 2000-01-01T00:00
        TIME_OFFSET = 946681200
        for_time += TIME_OFFSET
        return for_time // self.interval


class HOTP(OTP):
    def at(self, count):
        return self.generate_otp(count)

    def verify(self, otp, counter):
        return str(otp) == str(self.at(counter))