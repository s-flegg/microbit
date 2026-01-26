from microbit import *
import threading
from uart_microbit import Communicate
import radio

radio.on()
radio.config(length=251)

header = "ID, m_type, time, level, sessionID, accel, warning\n"
# used to share data between threads
data = []


def check_message_format(message):
    if "," in message:
        return True
    else:
        return False

def radio_output():
    while True:

        message = radio.receive()
        data.append(message)

        if message and check_message_format():
            # Debug to show when message is received
            display.show("R")

            send_message = header + message

            data.append(send_message)

def comms():
    uart = Communicate(False)

    while True:
        while len(data) > 0: # looping here will ensure termination doesn't happen while there are messages waiting to be sent
            uart.send(data.pop(0))
        uart.button_terminate()

t1 = threading.Thread(target=radio_output)
t2 = threading.Thread(target=comms)

t1.start()
t2.start()