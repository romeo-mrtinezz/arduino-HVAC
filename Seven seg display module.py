from pymata4 import pymata4
import time

arduino=pymata4.Pymata4()

SER=8
RCLK=9
SRCLK=10

firstDigitPin=7
secondDigitPin=6
thirdDigitPin=5
fourthDigitPin=4

sevenSegDigits=[firstDigitPin,secondDigitPin,thirdDigitPin,fourthDigitPin]

digitalPins=[4,5,6,7,8,9,10]
for i in digitalPins:
    arduino.set_pin_mode_digital_output(i)


alphaNumericCode={
    "0": [1, 1, 1, 1, 1, 1, 0, 0],
    "1": [0, 1, 1, 0, 0, 0, 0, 0],
    "2": [1, 1, 0, 1, 1, 0, 1, 0],
    "3": [1, 1, 1, 1, 0, 0, 1, 0],
    "4": [0, 1, 1, 0, 0, 1, 1, 0],
    "5": [1, 0, 1, 1, 0, 1, 1, 0],
    "6": [1, 0, 1, 1, 1, 1, 1, 0],
    "7": [1, 1, 1, 0, 0, 0, 0, 0],
    "8": [1, 1, 1, 1, 1, 1, 1, 0],
    "9": [1, 1, 1, 1, 0, 1, 1, 0],
    "A": [1, 1, 1, 0, 1, 1, 1, 0],
    "B": [0, 0, 1, 1, 1, 1, 1, 0],
    "C": [1, 0, 0, 1, 1, 1, 0, 0],
    "D": [0, 1, 1, 1, 1, 0, 1, 0],
    "E": [1, 0, 0, 1, 1, 1, 1, 0],
    "F": [1, 0, 0, 0, 1, 1, 1, 0],
    "G": [1, 0, 1, 1, 1, 1, 0, 0],
    "H": [0, 1, 1, 0, 1, 1, 1, 0],
    "I": [1, 0, 0, 0, 1, 0, 0, 0],
    "J": [0, 1, 1, 1, 0, 0, 0, 0],
    "K": [1, 0, 1, 0, 1, 1, 1, 0],
    "L": [0, 0, 0, 1, 1, 1, 0, 0],
    "M": [1, 0, 1, 0, 1, 0, 1, 0],
    "N": [0, 0, 1, 0, 1, 0, 1, 0],
    "O": [0, 0, 1, 1, 1, 0, 1, 0],
    "P": [1, 1, 0, 0, 1, 1, 1, 0],
    "Q": [1, 1, 1, 0, 0, 1, 1, 0],
    "R": [0, 0, 0, 0, 1, 0, 1, 0],
    "S": [1, 0, 1, 1, 0, 1, 1, 0],
    "T": [0, 0, 0, 1, 1, 1, 1, 0],
    "U": [0, 0, 1, 1, 1, 0, 0, 0],
    "V": [0, 1, 1, 1, 1, 1, 0, 0],
    "W": [0, 1, 0, 1, 0, 1, 1, 0],
    "X": [0, 1, 1, 0, 1, 1, 1, 0],
    "Y": [0, 1, 1, 1, 0, 1, 1, 0],
    "Z": [1, 1, 0, 1, 0, 0, 1, 0],
    "-": [0, 0, 0, 0, 0, 0, 0, 0]

    }







# turn digits on
def turn_digits_on():
    arduino.digital_write(4,0)
    arduino.digital_write(5,0)
    arduino.digital_write(6,0)
    arduino.digital_write(7,0)

def turn_digit1_on():
    arduino.digital_write(7,0)
    arduino.digital_write(6,1)
    arduino.digital_write(5,1)
    arduino.digital_write(4,1)
def turn_digit2_on():
    arduino.digital_write(7,1)
    arduino.digital_write(6,0)
    arduino.digital_write(5,1)
    arduino.digital_write(4,1)
def turn_digit3_on():
    arduino.digital_write(7,1)
    arduino.digital_write(6,1)
    arduino.digital_write(5,0)
    arduino.digital_write(4,1)
def turn_digit4_on():
    arduino.digital_write(7,1)
    arduino.digital_write(6,1)
    arduino.digital_write(5,1)
    arduino.digital_write(4,0)
def turn_digits_off():
    arduino.digital_write(7,1)
    arduino.digital_write(6,1)
    arduino.digital_write(5,1)
    arduino.digital_write(4,1)

def seven_seg_SR(toDisplay,option="decimal"):
    if option=="decimal":
        alphaNumericCode[toDisplay][7]=1
        pass
    else:
        pass
    for i in reversed(range(len(alphaNumericCode[toDisplay]))):
        arduino.digital_write(SER,alphaNumericCode[toDisplay][i])
        arduino.digital_write(SRCLK,1)
        arduino.digital_write(SRCLK,0)
    arduino.digital_write(RCLK,1)
    arduino.digital_write(RCLK,0)
    alphaNumericCode[toDisplay][7]=0

def SRCLEAR_mimic():
    arduino.digital_write(SER,0)
    a=0
    while a<8:
  
        arduino.digital_write(SRCLK,1)
        time.sleep(1)
        arduino.digital_write(SRCLK,0)
        time.sleep(1)
        a+=1
    arduino.digital_write(RCLK,1)
    time.sleep(0.5)
    arduino.digital_write(RCLK,0)
    time.sleep(0.5)


def run_seven_seg(display):
    '''
    :param display: enter a 4 digit alphanumeric phrase

    '''
    # intialising all digits off
    for i in range(len(sevenSegDigits)):
        arduino.digital_write(sevenSegDigits[i],1)
    
    # turning paramater display into a list
    digits = list(display)

    # infinite loop i.e displaying numbers/letters
    while True:
        try:


            seven_seg_SR(digits[0],"no decimal")
            time.sleep(0.0000001)
            turn_digit1_on()
            time.sleep(0.0000001)

            turn_digits_off()
            time.sleep(0.0000001)


            seven_seg_SR(digits[1],"decimal")
            time.sleep(0.0000001)
            turn_digit2_on()
            time.sleep(0.0000001)

            turn_digits_off()
            time.sleep(0.0000001)
            
            seven_seg_SR(digits[2],"no decimal")
            time.sleep(0.0000001)
            turn_digit3_on()
            time.sleep(0.0000001)

            turn_digits_off()
            time.sleep(0.0000001)

            seven_seg_SR(digits[3],"no decimal")
            time.sleep(0.0000001)
            turn_digit4_on()
            time.sleep(0.0000001)

            turn_digits_off()
            time.sleep(0.000001)

        except KeyboardInterrupt:
            break
    time.sleep(0.01)
    SRCLEAR_mimic()


def run_seven_seg_scroll(display,duration):
    '''
    :param display: enter a 4 digit alphanumeric phrase
    :param duration: "speed" of scrolling in seconds
    '''
    # intialising all digits off
    for i in range(len(sevenSegDigits)):
        arduino.digital_write(sevenSegDigits[i],1)
    
    # turning paramater display into a list
    digits = list(display)
    digits.append("-")

    print(digits)
    startTime  = time.time()

    # infinite loop i.e displaying numbers/letters
    while True:
        try:
            while time.time()-startTime < duration:
                try:
                    seven_seg_SR(digits[0],"no decimal")
                    time.sleep(0.0000001)
                    turn_digit1_on()
                    time.sleep(0.0000001)

                    arduino.digital_write(7,1)
                    time.sleep(0.0000001)

                    seven_seg_SR(digits[1],"no decimal")
                    time.sleep(0.0000001)
                    turn_digit2_on()
                    time.sleep(0.0000001)

                    arduino.digital_write(6,1)
                    time.sleep(0.0000001)

                    seven_seg_SR(digits[2],"no decimal")
                    time.sleep(0.0000001)
                    turn_digit3_on()
                    time.sleep(0.0000001)

                    arduino.digital_write(5,1)
                    time.sleep(0.0000001)

                    seven_seg_SR(digits[3],"no decimal")
                    time.sleep(0.0000001)
                    turn_digit4_on()
                    time.sleep(0.0000001)

                    arduino.digital_write(4,1)
                    time.sleep(0.0000001)

                except KeyboardInterrupt:
                    time.sleep(0.01)
                    SRCLEAR_mimic()
                    break
            # looping the list
            digits.append(digits[0])
            digits.pop(0)
            startTime=time.time()

        except KeyboardInterrupt:
            break

run_seven_seg_scroll("IMAGES",2)




