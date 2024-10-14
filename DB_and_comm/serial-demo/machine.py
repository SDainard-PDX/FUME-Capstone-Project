# this is a mock UART class that is included in the micropython
# machine module. I believe that it accurately emmulates the
# functionality of the machine.UART class, but I am not 100%
# confident as I don't own a raspberry pi pico.

class UART:
    def __init__(self, *_):
        pass

    def readline(self):
        msg = input("UART.readline(): ")
        try:
            msg = msg.encode('ascii')
        except:
            print("invalid message")
            msg = b''
        return msg

    def write(self, msg):
        print(msg)

    def any(self):
        return 1 # always assumes message recieved for demo