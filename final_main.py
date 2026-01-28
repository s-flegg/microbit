from microbit import *
import radio
import music
import time
import machine
from acceleration import *

#configure
radio.config(channel=7, group=1, power=7) #highest power for better range
radio.on()
set_volume(2000)
#music.set_tempo(bpm=160)

#constant state values
IDLE = 0
SENDING = 1
RESPONDING = 2
HELP_COMING = 3

#initialise
state = IDLE
alert = False
#message_ID = 0

#Get unique microbit id
unique_bytes = machine.unique_id()
skier_id = int.from_bytes(unique_bytes, 'little') % 256  #converts bytes object into integer



while True:
    
    messages = ""
    
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #add to messages
                csv_line = "{},{},{},{},{},{},{},{}".format(skier_id,"sos",None,None,None,None,None,None)
                messages += csv_line + "\n"
                state = SENDING
                alert = True
                
    
    #Handle radio events + updating state and alert
    state, alert = handle_radio(state, alert)
    
    #Play alert if needed
    sound(alert)
    
    
    if state == IDLE:
        
        #acceleration readings
        state, alert, csv_line = accelerometerDetect(skier_id, state, alert)
        messages += csv_line + "\n"

    
        #check co2 and temp
        csv_line_1, csv_line_1 = environment_monitor()
        messages += csv_line_1 + "\n" + csv_line_2 + "\n"
        
    
    
    #send all messages to be sent
    radio.send(messages)
    
    sleep(300)

    
    


