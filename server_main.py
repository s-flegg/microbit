from microbit import *
from uart_microbit import Communicate
import radio

def check_message_format(message):
    if "," in message:
        return True
    else:
        return False

radio.on()
radio.config(channel=7, group=1, power=7, queue=20)

uart = Communicate(False, True)
header_sent = False

while True:
    if not header_sent:
        uart.send("SkierID, Type, Time, Level, SessionID, Acceleration, Warning")
        header_sent = True

    message = radio.receive()


    if message and check_message_format(message):
        message = message.replace("n", "None") # replace used to save space on radio messages
        uart.send(message)

