# b32dec.py
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
#
# Original file base64 from http://github.com/micropython/micropython-lib/base64
# But we need only base32decode functionality and we use ubinascii
# Copyright (C) The Micropython Contributors (http://github.com/micropython/micropython-lib) - MIT License
#
# Changes:
# - Raise generic exception
# - Use system ubinascii instead of binascii

from gc import collect

def _bytes_from_decode_data(s):
    if isinstance(s, str):
        try:
            return s.encode('ascii')
        except:
            raise ValueError('string argument should contain only ASCII characters')
    elif isinstance(s, (bytes, bytearray)):
        return s
    else:
        raise TypeError("argument should be bytes or ASCII string, not %s" % s.__class__.__name__)

def b32decode(s, casefold=False, map01=None):
    _b32alphabet = {
        0: b'A', 9: b'J', 18: b'S', 27: b'3',
        1: b'B', 10: b'K', 19: b'T', 28: b'4',
        2: b'C', 11: b'L', 20: b'U', 29: b'5',
        3: b'D', 12: b'M', 21: b'V', 30: b'6',
        4: b'E', 13: b'N', 22: b'W', 31: b'7',
        5: b'F', 14: b'O', 23: b'X',
        6: b'G', 15: b'P', 24: b'Y',
        7: b'H', 16: b'Q', 25: b'Z',
        8: b'I', 17: b'R', 26: b'2',
    }

    _b32rev = dict([(v[0], k) for k, v in _b32alphabet.items()])

    s = _bytes_from_decode_data(s)
    quanta, leftover = divmod(len(s), 8)
    if leftover:
        raise Exception('Incorrect padding')
    del leftover
    collect()
    if map01 is not None:
        map01 = _bytes_from_decode_data(map01)
        assert len(map01) == 1, repr(map01)
        s = s.translate(bytes.maketrans(b'01', b'O' + map01))
    del map01
    collect()
    if casefold:
        s = s.upper()
    del casefold
    collect()
    padchars = s.find(b'=')
    if padchars > 0:
        padchars = len(s) - padchars
        s = s[:-padchars]
    else:
        padchars = 0
    parts = []
    acc = 0
    shift = 35
    from ubinascii import unhexlify
    for c in s:
        val = _b32rev.get(c)
        if val is None:
            raise Exception('Non-base32 digit found')
        del val
        collect()
        acc += _b32rev[c] << shift
        shift -= 5
        if shift < 0:
            parts.append(unhexlify(bytes('%010x' % acc, "ascii")))
            acc = 0
            shift = 35
    del shift

    last = unhexlify(bytes('%010x' % acc, "ascii"))
    del unhexlify, acc
    collect()
    if padchars == 0:
        last = b''                      # No characters
    elif padchars == 1:
        last = last[:-1]
    elif padchars == 3:
        last = last[:-2]
    elif padchars == 4:
        last = last[:-3]
    elif padchars == 6:
        last = last[:-4]
    else:
        collect()
        raise Exception('Incorrect padding')
    parts.append(last)
    res = b''.join(parts)
    del parts, _b32alphabet, _b32rev, last
    collect()
    return res
