from pymata4 import pymata4
import time

arduino = pymata4.Pymata4()
arduino.set_pin_mode_sonar(9,10,timeout=2000)

while True:
    try:
        reading=arduino.sonar_read(9)
        print(f"distance= {reading[0]}")
        print(f"time= {round(reading[1],2)}")
        time.sleep(2)

    except KeyboardInterrupt:
        arduino.shutdown()
        break