from microbit import *
import radio
import music


IDLE = 0
SENDING = 1
RECEIVING = 2


def handle_radio(state, alert):
    incoming = radio.receive()       
    
    
    #IDLE - waiting for SOS
    if state == IDLE:
        if incoming == "SOS":
            state = RESPONDING
            alert = True
            return state, alert
                
    
    #SENDING - sending SOS, waiting for confirm signal and handling cancellation           
    elif state == SENDING:
        
        send_message("SOS")
        
        if incoming == "confirm":
            display.show(Image.YES)
            display.clear()
            sleep(500)
        
        if button_b.was_pressed():
            cancel_sos()
            state = IDLE
            alert = False
            display.scroll(Image.NO)
            sleep(500)
            display.clear
            return state, alert
        
    #RESPONDING - 
    elif state == RESPONDING:
        #if sos signal is cancelled
        if incoming == "cancel":
            state = IDLE
            alert = False
            display.show(Image.NO)
            sleep(500)
            display.clear()
            return state, alert
        
        elif button_a.was_pressed():
            send_message("confirm")
            state = IDLE
            alert = False
            
    return state, alert


def send_message(message):
    radio.send(message)
    
    
def cancel_sos():
    for i in range(20):
        radio.send("cancel")
        display.show(Image.NO)
        display.clear()
        
        
def sound(sound_active):
    if sound_active:
        music.play(music.WAWAWAWAA, wait=False)
        sleep(1000) #play once per second
            