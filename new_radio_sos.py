from microbit import *
import radio
import music


IDLE = 0
SENDING = 1
RESPONDING = 2
HELP_COMING = 3


def handle_radio(state, alert):
    """ Used to handle SOS finite state machine. This funciton is called once every loop.
                        
                                                 IDLE
        All microbits stay in IDLE state where they are constantly able to receive transmissions.
        In this state, other features also function.
        
        If an "SOS" radio signal is received, state is switched to RESPONDING and the alert sound
        is activated
        
        
        If button B is pressed, state is switched to SENDING and the alert sound is activated.
        
        
                                               SENDING
        When in SENDING state, all other features should be deactivated. An SOS signal is sent once
        every loop. If a "confirm" radio signal is received, a tick appears on screen. Press button B to
        cancel sos signal at any time. This sends out a "cancel" radio signal, switchs to IDLE state
        again and turns off the alert sound.
        
        
                                              RESPONDING
        When in RESPONDING state, all other features should be deactivated. If button A is pressed, a
        "confirm" radio signal is sent to acknowledge the distress signal and the state is switched to
        HELP_COMING and alert sound is turned off. If a "cancel" radio signal is detected before they can
        accept, state is switched to IDLE and alert sound is turned off.
        
                                              HELP_COMING
        This is essentially a transitionary state. From the RESPONDING state, if switched to IDLE after
        sending "confirm", the microbit will pick up the "sos" signal again. So instead it switches to the
        HELP_COMING state where no "sos" signals are detected. If a "cancel" radio signal is detected or
        button B is pressed then the state is switched to IDLE.
        
        
        """
    
    
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
            send_cancel()
            state = IDLE
            alert = False
            display.show(Image.NO)
            sleep(500)
            display.clear()
            return state, alert
        
    #RESPONDING - 
    elif state == RESPONDING:
        
        display.scroll("SOS", wait=False)
        
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
            state = HELP_COMING # need extra "limbo" state so sos signal isn't picked up again
            alert = False
            
    #HELP COMING
    elif state == HELP_COMING:
        if incoming == "cancel":
            state = IDLE
            display.show(Image.NO)
            sleep(500)
            display.clear()
            return state, alert
        
        if button_b.was_pressed():
            send_cancel()
            state = IDLE
            alert = False
            display.show(Image.NO)
            sleep(500)
            display.clear()
            return state, alert
        
    return state, alert


def send_message(message):
    radio.send(message)
    
    
def send_cancel():
    for i in range(20):
        radio.send("cancel")
        display.show(Image.NO)
        display.clear()
        
        
def sound(sound_active):
    if sound_active:
        music.play(music.WAWAWAWAA, wait=False)
        sleep(1000) #play once per second
            








