# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

import os
import json

class Storage():
    def __init__(self, file):
        self.file = file
        self._intent_prefix = '~'

    def get_or_create(self):
        try:
            with open(self.file, 'r') as f:
                data = f.read()
            return json.loads(data)
        except:
            print('Storage not found')
            storage = dict()
            self.save(storage)
        return storage

    def get(self):
        with open(self.file, 'r') as f:
            data = f.read()
        return json.loads(data)

    def save(self, storage):
        s = json.dumps(storage)
        with open(self._intent_prefix + self.file, 'w') as f:
            f.write(s)
        os.rename(self._intent_prefix + self.file, self.file)