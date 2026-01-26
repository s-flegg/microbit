from microbit import *
import radio
import music
#from bme688 import *
#from OLED import *
from Radio_SOS import *
import time
#import datetime


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
READ_ACCEL = 4

#initialise
state = IDLE
alert = False
message_ID = 0



while True:
    
    messages = ""
    
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #add to messages
                #messages += ID + ", sos, " + str(datetime.datetime.now()) + ", None, None, None\n"
                state = SENDING
                alert = True
                
    
    #Handle radio events + updating state and alert
    state, alert = handle_radio(state, alert)
    
    #Play alert if needed
    sound(alert)
    
    
    #if state == IDLE or state == READ_ACCEL:
        
        #check for button a press
            #state = read_accel
        
            #acceleration readings
            #add to messages
            #messages += ID + ", accel, " + str(datetime.datetime.now()) + ", None, " + str(session_ID) + ", " + str(accel) + "\n"
            
        
        #check co2 and temp
        
        
    
    
    
    
    
    #send all messages to be sent
    if messages:
        radio.send(messages)
    
    sleep(300)

    
    


