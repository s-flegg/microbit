from microbit import *
import music
from bme688 import *
from OLED import *

# Threshold values
CO2_THRESHOLD = 1000          # ppm 1500
TEMP_THRESHOLD = -20        # °C (dangerous cold for skiing)
READ_INTERVAL = 60000         # 1 minute

# Initialise sensor
init_sensor()
init_gas_sensor()
sleep(2000)
establish_baselines()
init_display()

def environment_monitor(skier_id=1):
    # Get current time in seconds
    current_time = running_time() // 1000

    # Read sensor values
    read_data_registers()
    iaqScore, iaqPercent, eCO2 = calc_air_quality()
    temperature = calc_temperature()

    # Display values on OLED
    show("CO2: {}ppm".format(eCO2), 0)
    show("TEMP: {}C".format(int(temperature)), 2)

   # Temperature warning
    if temperature <= TEMP_THRESHOLD:
        display.show(Image.XMAS)

        # Temperature warning sound
        music.play([
            'E4:2', 'C4:2',
            'E4:2', 'C4:2'
        ])
        
        temp_status = "D"

    else:
        temp_status = "S"

    # CO2 warning
    if eCO2 >= CO2_THRESHOLD:
        display.show(Image.SKULL)

        # CO2 warning sound (not SOS)
        music.play([
            'C4:2', 'C4:2', 'C4:2',
            'R:1',
            'C4:2'
        ])
        co2_status = "D"    
    else:
        co2_status = "S"
    
    display.show(Image.YES)
    
    return "{},TEMP,{},{},{},{},{}".format(skier_id, current_time, temperature, "n", "n", temp_status), "{},CO2,{},{},{},{},{}".format(skier_id, current_time, eCO2,"n","n",co2_status)


        
    #(id,mtype,time,level,sessionid,accel, warning)
