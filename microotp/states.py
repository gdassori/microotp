# MicroPython One Time Password Generator
# Copyright (C) 2016 Guido Dassori <guido.dassori@gmail.com>
# MIT License

from settings import WIFI_TIMEOUT


class State():
    __NAME = ''
    def on_enter(self, owner):
        print('Enter {}'.format(self.__NAME))

    def on_exit(self, owner):
        print('Exit {}'.format(self.__NAME))
        pass


class InitState(State):
    __NAME = 'InitState'
    def __init__(self):
        self.bootstrap_state = None
        self.otp_state = None

    def on_enter(self, owner):
        super().on_enter(owner)
        owner.set_state(self)
        if owner.ready:
            self.otp_state.on_enter(owner)
            return
        self.bootstrap_state.on_enter(owner)


class BootstrapState(State):
    __NAME = 'BootstrapState'
    def __init__(self):
        self.otp_state = None
        self.sleep_state = None

    def on_enter(self, owner):
        super().on_enter(owner)
        owner.set_state(self)
        if owner.ready:
            self.otp_state.on_enter(owner)
            return
        if not owner.bootstrap(WIFI_TIMEOUT):
            self.sleep_state.on_enter(owner)


class ShowOTPState(State):
    __NAME = 'OTPState'
    def __init__(self):
        self.sleep_state = None

    def on_enter(self, owner):
        super().on_enter(owner)
        owner.set_state(self)
        owner.show_current_otp()
        self.sleep_state.on_enter(owner)


class SleepState(State):
    __NAME = 'SleepState'
    def on_enter(self, owner):
        super().on_enter(owner)
        if owner.data_changed:
            owner.save_storage()
        owner.sleep()


def init():
    init_state = InitState()
    bootstrap_state = BootstrapState()
    otp_state = ShowOTPState()
    sleep_state = SleepState()

    init_state.bootstrap_state = bootstrap_state
    init_state.otp_state = otp_state
    bootstrap_state.otp_state = otp_state
    bootstrap_state.sleep_state = sleep_state
    otp_state.sleep_state = sleep_state

    return init_state
