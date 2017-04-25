# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from gc import collect


class OTPManager():
    def __init__(self, otp_data):
        self.otp_data = otp_data

    def get_ttl(self):
        from utime import time
        now = time()
        res = (now + (30 - now % 30)) - now
        del time, now
        collect()
        return res

    def get_code(self):
        if self.otp_data.get('type', 'TOTP') == 'OTP':
            from otp import OTP as O
            totp = O(self.otp_data['seed'])
            res = totp.generate_otp(self.otp_data['input'])
        else:
            from otp import TOTP as O
            totp = O(self.otp_data['seed'])
            res = totp.now()
        del O, totp
        collect()
        return res

    def get_alias(self):
        return self.otp_data['alias']