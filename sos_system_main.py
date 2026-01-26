from microbit import *
import radio
import music
import machine
from acceleration_pc import *
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

#Get unique microbit id
unique_bytes = machine.unique_id()
skier_id = int.from_bytes(unique_bytes, 'little') % 256  #converts bytes object into integer

while True:
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #send_sos_data(ID, time)
                state = SENDING
                alert = True
                
    
    #Handle accelerometer and radio events
    state, alert = accelerometerDetect(skier_id, state, alert)
    
    #Sleep a short time between
    sleep(500)
