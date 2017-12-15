def recv(socket, size):
    data = b''
    while size > 0:
        try:
            _data = socket.recv(size)
            if _data:
                size -= len(_data)
                data += _data
            else:
                raise OSError()
        except OSError as e:
            if str(e) == 'timed out':
                continue
            else:
                return b''
        except Exception as e:
            print(e)
            return b''

    return data

def send(socket, data, size):
    while size > 0:
        try:
            size -= socket.send(data[:size])
        except OSError as e:
            print(e)
            break
        except Exception as e:
            print(e)
            break

    return size == 0