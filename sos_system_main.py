from microbit import *
import radio
import music
from new_radio_sos import *

#configure
radio.config(channel=7, group=1, power=7) #highest power for better range
radio.on()
set_volume(100)
#music.set_tempo(bpm=160)

#constant state values
IDLE = 0
SENDING = 1
RESPONDING = 2

#initialise
state = IDLE
alert = False


while True:
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #send_sos_data(ID, time)
                state = SENDING
                alert = True
                
    
    #Handle radio events + updating state and alert
    state, alert = handle_radio(state, alert)
    
    #Play alert if needed
    sound(alert)
    
    sleep(300)

    
    



