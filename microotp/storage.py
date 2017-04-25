# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from gc import collect

class Storage():
    # TODO use json only in setup mode, store binary data
    def __init__(self, file):
        self.file = file
        self._intent_prefix = '~'

    def get_or_create(self):
        from json import loads
        try:
            return self.get()
        except:
            del loads
            collect()
            storage = dict()
            self.save(storage)
        return storage

    def get(self):
        from json import loads
        from ubinascii import unhexlify
        with open(self.file, 'r') as f:
            data = f.read()
        res = loads(data)
        for otp in res['otp']['rows']:
            otp['seed'] = unhexlify(otp['seed'])
        del loads, f, data, unhexlify
        collect()
        return res

    def save(self, storage):
        from json import dumps
        s = dumps(storage)
        with open(self._intent_prefix + self.file, 'w') as f:
            f.write(s)
        from os import rename
        rename(self._intent_prefix + self.file, self.file)
        del dumps, f, rename
        collect()