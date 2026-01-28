from microbit import *
import music
from bme688 import *
from OLED import *

# Threshold values
CO2_THRESHOLD = 1500          # ppm
TEMP_THRESHOLD = -10          # °C (dangerous cold for skiing)
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

    # CO2 warning
    if eCO2 >= CO2_THRESHOLD:
        display.show(Image.SKULL)

        # CO2 warning sound (not SOS)
        music.play([
            'C4:2', 'C4:2', 'C4:2',
            'R:1',
            'C4:2'
        ])

        return {
            "skier_id": skier_id,
            "time": current_time,
            "co2": eCO2,
            "temperature": temperature,
            "warning": "CO2"
        }

    # Temperature warning
    if temperature <= TEMP_THRESHOLD:
        display.show(Image.XMAS)

        # Temperature warning sound
        music.play([
            'E4:2', 'C4:2',
            'E4:2', 'C4:2'
        ])

        return {
            "skier_id": skier_id,
            "time": current_time,
            "co2": eCO2,
            "temperature": temperature,
            "warning": "TEMP"
        }

    # Safe conditions
    display.show(Image.YES)
    return None

environment_monitor()