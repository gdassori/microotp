# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License


def rem(t,l):
    return '.' * int((8/t)*l) + '.'


DATETIME_LINE = 'line0'

Views = dict(
    network = dict(
        wait = lambda token, timeout, ttl: dict(
            line0='Open the APP and',
            line1='enter code {}'.format(token),
            line2=rem(timeout, ttl)
        ),
        connected = lambda: dict(
            line0='Connected',
            line1='Setup mode',
        )
    ),
    otp = lambda otp_tuple: dict(
        line1='{}'.format(otp_tuple[0]),
        line2='{}'.format(otp_tuple[1]),
        line2b=rem(30, otp_tuple[2])
    )
)

def get_datestring():
    from gc import collect
    from machine import RTC
    d = RTC().datetime()
    del RTC
    res = "{}-{}-{} {}:{}:{}".format(str(d[0])[2:], d[1], d[2], d[4], d[5], d[6])
    collect()
    return res