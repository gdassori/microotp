# Original file base64 from http://github.com/micropython/micropython-lib/base64
# But we need only base32decode functionality and we use ubinascii
# Copyright (C) The Micropython Contributors (http://github.com/micropython/micropython-lib) - MIT License


from gc import collect


def translate(d, t):
    return b''.join([bytes([t[x]]) for x in d])

digest_size = None


class HMAC:
    blocksize = 64
    def __init__(self, key, msg=None, digestmod=None):
        from utime import sleep
        self.finished = False
        self.digest_bytes = None
        self.hex_bytes = None
        assert digestmod
        self.digest_cons = digestmod

        if not isinstance(key, (bytes, bytearray)):
            raise TypeError()

        self.outer = self.digest_cons()
        self.inner = self.digest_cons()
        if str(self.inner) == '<sha1>':
            self.digest_size = 20
        elif str(self.inner) == '<sha256>':
            self.digest_size = 32
        else:
            self.digest_size = None

        blocksize = self.blocksize
        self.block_size = blocksize

        if len(key) > blocksize:
            key = self.digest_cons(key).digest()

        key = key + bytes(blocksize - len(key))
        trans_5C = bytes((x ^ 0x5C) for x in range(256))
        trans_36 = bytes((x ^ 0x36) for x in range(256))
        self.outer.update(translate(key, trans_5C))
        del trans_5C
        collect()
        sleep(0.1)
        self.inner.update(translate(key, trans_36))
        del trans_36, key, sleep
        collect()
        if msg is not None:
            self.update(msg)

    @property
    def name(self):
        return "hmac-" + str(self.inner)[1:-1:]

    def update(self, msg):
        if not self.finished:
            self.inner.update(msg)
        else:
            raise ValueError()

    def _current(self):
        self.outer.update(self.inner.digest())
        return self.outer

    def digest(self):
        if not self.finished:
            h = self._current()
            self.digest_bytes = h.digest()
            self.finished = True
        return self.digest_bytes

def new(key, msg=None, digestmod=None):
    return HMAC(key, msg, digestmod)