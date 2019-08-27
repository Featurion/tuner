# General

SERVER_VERSION = 'dev'

# Message Types

Msg2Code = {
    'CLIENT_HELLO': 1,
    'CLIENT_HELLO_RESP': 2,
    'CLIENT_EJECT': 3,
    'CLIENT_VIEW_SET': 10,
    'CLIENT_VIEW_REQ': 11,
    'CLIENT_FRAME': 12
}
Code2Msg = {v: k for k, v in Msg2Code.items()}
globals().update(Msg2Code)
