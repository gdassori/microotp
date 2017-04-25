# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from gc import collect

class Storage():
    def __init__(self, file):
        self.file = file
        self._intent_prefix = '~'

    def get_or_create(self):
        from json import loads
        try:
            with open(self.file, 'r') as f:
                data = f.read()
            res = loads(data)
            del loads, f, data
            collect()
            return res
        except:
            if getattr(__name__, 'f', None): del f
            if getattr(__name__, 'data', None): del data
            del loads
            collect()
            print('Storage not found')
            storage = dict()
            self.save(storage)
        return storage

    def get(self):
        from json import loads
        with open(self.file, 'r') as f:
            data = f.read()
        res = loads(data)
        del loads, f, data
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