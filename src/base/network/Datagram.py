class Datagram(dict):

    def __init__(self, **kwargs):
        super().__init__()
        self.update(kwargs)

    def __getattr__(self, key):
        if key in self:
            return self[key]
        else:
            raise AttributeError

    def __setattr__(self, key, val):
        try:
            val = super().__getattribute__(key)
        except AttributeError:
            self[key] = val
        else:
            raise AttributeError('cannot override %s' % repr(val))
