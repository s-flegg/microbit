from microbit import *
from uart_microbit import Communicate
import radio

radio.on()
radio.config(length=251)

header = "ID, m_type, time, level, sessionID, accel, warning\n"

uart = Communicate(False, True)

def check_message_format(message):
    if "," in message:
        return True
    else:
        return False

while True:

    message = radio.receive()

    if message and check_message_format(message):
        # Debug to show when message is received
        display.show("R")

        send_message = header + message

        uart.send(send_message)
