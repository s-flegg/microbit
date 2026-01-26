from microbit import *
import radio


radio.on()
radio.config(length=251)

def check_message_format(message):
    if "," in message:
        return True
    else:
        return False
        
  
header =  "ID, m_type, time, level, sessionID, accel, warning\n"
   
while True:
    
    message = radio.receive()

    
    if message and check_message_format():
        #Debug to show when message is received
        display.show("R")
        
        send_message = header + message
        
        radio.send(send_message)
        
        
    sleep(500)