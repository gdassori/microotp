# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

import os
import json
import btree


class BTree():
    def __init__(self):
        self.file = 'btree.db'
        self._intent_prefix = '~'

    def get(self, value):
        try:
            with open(self.file, 'r+b') as f:
                db = btree.open(f)
                value = db[value]
            return value.decode()
        except:
            return None

    def set(self, key, value):
        with open(self.file, 'w+b') as f:
            db = btree.open(f)
            db[key.encode()] = str(value).encode()
            db.flush()


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

    @property
    def btree(self):
        return BTree()
