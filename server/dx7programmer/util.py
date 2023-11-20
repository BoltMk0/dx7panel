
def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val                         # return positive value as is


def generate_checksum(data: bytes):
    s = sum([int(i) for i in data])
    return -s & 0x7F


class Signal:
    def __init__(self):
        self._cbs = []

    def register_cb(self, cb):
        self._cbs.append(cb)

    def unregister_cb(self, cb):
        self._cbs.remove(cb)

    def connect(self, cb):
        self.register_cb(cb)

    def disconnect(self, cb):
        self.unregister_cb(cb)

    def emit(self, *args):
        for cb in self._cbs:
            cb(*args)

    def clear(self):
        self._cbs.clear()

    def __call__(self, *args, **kwargs):
        self.emit(*args)
