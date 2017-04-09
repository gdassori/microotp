# Original file base64 from http://github.com/micropython/micropython-lib/base64
# But we need only base32decode functionality and we use ubinascii
# Copyright (C) The Micropython Contributors (http://github.com/micropython/micropython-lib) - MIT License

import uhashlib as _hashlib


trans_5C = bytes((x ^ 0x5C) for x in range(256))
trans_36 = bytes((x ^ 0x36) for x in range(256))


def translate(d, t):
    return b''.join([bytes([t[x]]) for x in d])


digest_size = None


class HMAC:
    blocksize = 64
    def __init__(self, key, msg=None, digestmod=None):
        self.finished = False
        self.digest_bytes = None
        self.hex_bytes = None

        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("key: expected bytes or bytearray, but got %r" % type(key).__name__)

        if digestmod is None:
            digestmod = _hashlib.sha256

        if callable(digestmod):
            self.digest_cons = digestmod
        elif isinstance(digestmod, str):
            self.digest_cons = lambda d=b'': getattr(_hashlib, digestmod)(d)
        elif isinstance(digestmod, (bytes, bytearray)):
            self.digest_cons = lambda d=b'': getattr(_hashlib, str(digestmod)[2:-1:])(d)
        else:
            self.digest_cons = lambda d=b'': digestmod.new(d)

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
        self.outer.update(translate(key, trans_5C))
        self.inner.update(translate(key, trans_36))
        if msg is not None:
            self.update(msg)

    @property
    def name(self):
        return "hmac-" + str(self.inner)[1:-1:]

    def update(self, msg):
        if not self.finished:
            self.inner.update(msg)
        else:
            raise ValueError('Currently, a digest can only be generated once. '
                             'This object is now "spent" and cannot be updated.')

    def _current(self):
        self.outer.update(self.inner.digest())
        return self.outer

    def digest(self):
        if not self.finished:
            h = self._current()
            self.digest_bytes = h.digest()
            import ubinascii
            self.hex_bytes = ubinascii.hexlify(self.digest_bytes)
            del(ubinascii)
            self.finished = True
        return self.digest_bytes

    def hexdigest(self):
        if not self.finished:
            h = self._current()
            self.digest_bytes = h.digest()
            import ubinascii
            self.hex_bytes = ubinascii.hexlify(self.digest_bytes)
            del(ubinascii)
            self.finished = True
        return self.hex_bytes


def new(key, msg=None, digestmod=None):
    return HMAC(key, msg, digestmod)


def compare_digest(a, b, double_hmac=True, digestmod=b'sha256'):
    if not isinstance(a, (bytes, bytearray)) or not isinstance(b, (bytes, bytearray)):
        raise TypeError("Expected bytes or bytearray, but got {} and {}".format(type(a).__name__, type(b).__name__))

    if len(a) != len(b):
        raise ValueError("This method is only for comparing digests of equal length")

    if double_hmac:
        try:
            import uos
            nonce = uos.urandom(64)
        except ImportError:
            double_hmac = False
        except AttributeError:
            double_hmac = False

    if double_hmac:
        a = new(nonce, a, digestmod).digest()
        b = new(nonce, b, digestmod).digest()

    result = 0
    for index, byte_value in enumerate(a):
        result |= byte_value ^ b[index]
    return result == 0