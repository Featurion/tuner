# General

SERVER_VERSION = 'dev'
BROADCAST_CHANNEL_MIN = 100

# Message Types

Msg2Code = {
    'CLIENT_HELLO': 1,
    'CLIENT_HELLO_RESP': 2,
    'CLIENT_EJECT': 3,
    'CLIENT_STREAM_REQ': 10,
    'CLIENT_STREAM_REQ_RESP': 11,
    'CLIENT_STREAM_DONE': 12,
    'CLIENT_VIEW_REQ': 13,
    'CLIENT_VIEW_REQ_RESP': 14,
    'CLIENT_VIEW_DONE': 15,
    'CLIENT_FRAME': 16,
}
Code2Msg = {v: k for k, v in Msg2Code.items()}
globals().update(Msg2Code)
