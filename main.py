from microbit import *
import radio
import music
import time
import machine
from acceleration import *
from data_warning import *

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
    current_time = running_time() // 1000
    
    
    #SOS SYSTEM
    
    #Start sending SOS
    if state == IDLE and button_b.was_pressed():
                #add to messages
                csv_line = "{},{},{},{},{},{},{},{}".format(skier_id,"sos",current_time,"n","n","n","n","n")
                messages += csv_line + "\n"
                radio.send(csv_line)
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
        radio.send(csv_line)

    
        #check co2 and temp
        csv_line_1, csv_line_2 = environment_monitor(skier_id)
        messages += csv_line_1 + "\n" + csv_line_2 + "\n"
        radio.send(csv_line_1)
        radio.send(csv_line_2)
        
    
    
    #send all messages to be sent
    print(messages)
    
    sleep(300)

    
    


