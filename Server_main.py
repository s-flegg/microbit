from microbit import *
import uart_microbit
import radio

def check_message_format(message):
    if "," in message:
        return True
    else:
        return False

radio.on()
radio.config(channel=7, group=1, power=7)

uart = uart_microbit.Communicate(False, True)
header_sent = False

while True:
    if not header_sent: # uart.send must be used in a loop, this flag ensures the header is only sent once
        uart.send("SkierID, Type, Time, Level, Warning, SessionID, Acceleration, GForce")
        header_sent = True

    message = radio.receive()

    if message and check_message_format(message):
        uart.send(message)

