# sha1.py
#
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License
#

from gc import collect


def translate(d, t):
    return b''.join([ chr(t[x]).encode('ascii') for x in d ])

digest_size = None

class sha1:
    digest_size = digestsize = 32
    block_size = 20

    def __init__(self, s=None):
        from uhashlib import sha1 as usha1
        self._s = s
        self.name = 'sha1'
        self.usha1 = self._s and usha1(self._s) or None
        del usha1
        collect()

    def update(self, s):
        from uhashlib import sha1 as usha1
        self._s = self._s and '%s%s' % (self._s, s) or s
        if self.usha1:
            self.usha1.update(s)
        else:
            self.usha1 = usha1(self._s)
        del usha1
        collect()

    def digest(self):
        if self.usha1:
            return self.usha1.digest()

    def copy(self):
        return sha1(s=self._s)