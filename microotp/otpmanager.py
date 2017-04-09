# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

import utime


class OTPManager():
    def __init__(self, otp_list, pos):
        self.otp_list = otp_list
        self.pos = pos

    def next_otp(self):
        return OTPManager(
            self.otp_list,
            not self.pos+1 >= len(self.otp_list) and self.pos +1 or 0
        )

    def prev_otp(self):
        return OTPManager(
            self.otp_list,
            not self.pos-1 < 0 and self.pos-1 or len(self.otp_list)-1
        )

    @property
    def ttl(self):
        now = utime.time()
        return (now + (30 - now % 30)) - now

    @property
    def code(self):
        return self.otp_list[self.pos]['seed'] # TODO

    @property
    def alias(self):
        return self.otp_list[self.pos]['alias']