from pymata4 import pymata4
import time
import math

board = pymata4.Pymata4()
thermistorPin = 0
realValues=[0.001]


board.set_pin_mode_analog_input(thermistorPin)

while True: 
    try:
        read1=board.analog_read(thermistorPin)
        read2=board.analog_read(thermistorPin)
        read3=board.analog_read(thermistorPin)
        
        averageRead=(read1[0]+read2[0]+read3[0])/3+0.0001
        print(averageRead)
        averagedTemp=-21.21*math.log((10*((1024/averageRead)-1)))+72.203
        realValues.append(averagedTemp)
        print (f"temperature= {averagedTemp}")
        time.sleep(1)

            
    except KeyboardInterrupt:
        break



