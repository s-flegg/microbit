from microbit import *
import radio
import music
import time
from Radio_SOS import *
from data_warning import *
from acceleration.py import *

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



while True:
    
    messages = ""
    
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #add to messages
                csv_line = "{},{},{:.2f},{},{},{},{:.2f},{:.2f}".format(skier_id,"sos",datetime.datetime.now(),None,None,None,None,None)
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
    if messages:
        radio.send(messages)
    
    sleep(300)

    
    


