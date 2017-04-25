# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License


from settings import WIFI_TIMEOUT, NET_GATEWAY, NET_IP, NET_NETMASK, NET_DNS, NET_SSID
from network import STA_IF, WLAN
from gc import collect


class WiFiContext():
    def __init__(self, network):
        self.net = network

    def __enter__(self):
        self.net.enable()
        self.net.connect()
        return self

    def __exit__(self, type, value, traceback):
        self.net.disable()


class WiFi():
    def __init__(self):
        self.timeout = 60
        self.net = WLAN(STA_IF)
        self._ssid = self._password = None
        self.token = None

    def _get_network(self):
        raise NotImplementedError

    def get_network_token(self):
        from os import urandom
        r = str(int.from_bytes(urandom(2), 'little'))
        t = '0' * (4 - len(r)) + r
        del urandom, r
        collect()
        return t[:4]

    def Context(self, timeout):
        self.timeout = timeout
        self.token = self.get_network_token()
        if NET_SSID:
            self._ssid, self._password = NET_SSID.split('|')
        else:
            self._get_network()
        return WiFiContext(self)

    @property
    def connected(self):
        isc = self.net.isconnected()
        print('Is connected? {}'.format(isc))
        return isc

    def enable(self):
        self.net.active(True)

    def connect(self, ssid=None, password=None, timeout=WIFI_TIMEOUT):
        ssid = self._ssid or ssid
        password = self._password or password
        self.net.ifconfig(((NET_IP, NET_NETMASK, NET_GATEWAY, NET_DNS)))
        self.net.connect(ssid, password)

    def disable(self):
        from gc import collect
        from network import AP_IF
        self.net.active(False)
        WLAN(AP_IF).active(False) # Always ensure AP is disabled
        del AP_IF
        collect()

    def send_data(self, topic, data):
        pass

    def get_data(self, topic):
        pass