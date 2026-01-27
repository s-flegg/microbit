from microbit import *
import time
from new_radio_sos import *  


# Store session info internally
session = {
    "active": False,
    "id": None,
    "start_time": None
}


def next_session_id():
    # Read last session from file
    try:
        with open("session.txt", "r") as f:
            current = int(f.read())
    except OSError:
        current = 0  # if file doesn't exist

    # Increment session
    new_session = (current + 1) % 256

    # Save new session back to file
    with open("session.txt", "w") as f:
        f.write(str(new_session))

    return new_session


def accelerometerDetect(skier_id, state, alert):
    accelerometer.set_range(8)  # 8g max per axis, therefore max g = 13.86

    # Session toggle with button A
    if button_a.was_pressed():  
        if not session["active"]:
            # Start session
            session["active"] = True
            session["id"] = next_session_id()
            session["start_time"] = running_time()
            display.scroll("Start")
        else:
            # Stop session
            session["active"] = False
            display.scroll("Stop")

    # If session is active, calculate acceleration and send data
    if session["active"]:
        # Calculate acceleration
        g_force = accelerometer.get_strength() / 1000
        elapsed_time = (running_time() - session["start_time"]) / 1000  # seconds
        acceleration_mps2 = g_force * 9.80665

        # CSV format for radio
        csv_line = "{},{},{:.2f},{},{},{},{:.2f}".format(skier_id, "accel", elapsed_time, None, None, session["id"], acceleration_mps2)
        
        # SOS alert if g_force > 8
        if g_force > 8 and state != SENDING:
            # Start SOS automatically if severe g_force
            state = SENDING
            alert = True

    # Handle SOS radio events and update alert
    state, alert = handle_radio(state, alert)


    # Return updated state and alert
    return state, alert, csv_line

