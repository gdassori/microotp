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
    otp = lambda otp: dict(
        line1='{}'.format(otp.alias),
        line2='{}'.format(otp.code),
        line2b=rem(30, otp.ttl)
    )
)

def format_datetime(datetime):
    return "{}-{}-{} {}:{}:{}".format(
        str(datetime[0])[2:],
        datetime[1],
        datetime[2],
        datetime[4],
        datetime[5],
        datetime[6]
    )