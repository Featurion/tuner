import re

from ...base.constants import Msg2Code


class MetaHandler(type):

    prefix = 'r_handle'

    def __new__(cls, clsname, bases, dct):
        clstype = super().__new__(cls, clsname, bases, dct)
        clstype.handlers = {}

        if not getattr(clstype, 'msgtype'):
            return clstype

        for cls in bases:
            clstype.handlers.update(getattr(cls, 'handlers', {}))

        for name, val in dct.items():
            if name.startswith(MetaHandler.prefix):
                camel = name.rsplit(MetaHandler.prefix)[-1]
                words = re.findall('[A-Z][a-z]+', camel)
                words.insert(0, clstype.msgtype)
                msgname =  '_'.join(words).upper()

                try:
                    code = Msg2Code[msgname]
                    clstype.handlers[code] = name
                except KeyError:
                    continue

        return clstype
