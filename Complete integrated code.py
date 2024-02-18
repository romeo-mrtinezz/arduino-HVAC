"""
Purpose: This module provides the functionaliy required to operate a HVAC System 

The following code includes the use of:
- shift register to conduct a seven seg display
- motor driver to simulate fans
- thermistors to read temperature
- ultrasonic sensor to read distance
- another shift register to simulate a thermometer via LEDs


    
Author: Mateysh Naidu, Romeo Martinez, Iordanis Sapountzis, Rahul Sahni, Hari Senthuran
Date Created: 4/05/2023
Last Modified: 21/05/2023
Version: lost count
"""

# Initializing variables
correctPin = 1234
desiredTemperatureRange = [16,17] # degrees celsius
temperatureData = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.001]  #or 20 0s?
secondtemperatureData = [0.001]
avgResistance = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
avgDistance = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
multiplier = 1

import time
import random
import math
import matplotlib.pyplot as plt
from pymata4 import pymata4

arduino = pymata4.Pymata4()

###----------------------------------------Initialising Pins for shift register and 7 Segment Display--------------------------------------------------------------------------------------

# Initialising Pins for shift register and 7 Segment Display
SER=8
RCLK=9
SRCLK=10

firstDigitPin=7
secondDigitPin=6
thirdDigitPin=5
fourthDigitPin=4

digitalPins=[4,5,6,7,8,9,10]
for i in digitalPins:
    arduino.set_pin_mode_digital_output(i)

sevenSegDigits=[firstDigitPin,secondDigitPin,thirdDigitPin,fourthDigitPin]
# -----Initialising pins for ultrasonic and buzzer----------
trigPin = 17
echoPin = 18
arduino.set_pin_mode_sonar(trigPin,echoPin,timeout=2000)

tonePin=19 # buzzer
arduino.set_pin_mode_tone(tonePin)


###----------------------------------------initialising pins for LED SR --------------------------------------------------------------------------------------
#initialising pins for LED SR 

    # Pin mappings for shift register
SERLED = 2   # Serial data input
SRCLKLED = 3  # Shift register clock
RCLKLED = 14      # Register clock

pinsUsed= [SERLED, SRCLKLED, RCLKLED]

for pin in pinsUsed:
    arduino.set_pin_mode_digital_output(pin)


###------------------------------------Initialising Pins for Fan Control--------------------------------------------------------------------------------------
fanEnablePin=11
fan1=12
fan2=13

arduino.set_pin_mode_pwm_output(fanEnablePin)
arduino.set_pin_mode_digital_output(fan1)
arduino.set_pin_mode_digital_output(fan2)

# Initialising Thermistor Pin (analogue) 
thermistorPin=1
thermistorPin2=2
arduino.set_pin_mode_analog_input(thermistorPin)
arduino.set_pin_mode_analog_input(thermistorPin2)


# Initialises the AlphaNumberic Code for the 7-segment display 
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



def safety_interlock():
    """
    safety_interlock function detects when an object enters the enclosed space and sounds a buzzer
    Inputs: 
        None
    Return:
        None
    """
    global avgDistance
    arduino.sonar_read(trigPin)
    arduino.sonar_read(trigPin)
    while True:
        try:
            read1=arduino.sonar_read(trigPin)
            read2=arduino.sonar_read(trigPin)
            read3=arduino.sonar_read(trigPin)
            avgRead = (read1[0]+read2[0]+read3[0])/3
            avgDistance.append(avgRead)
            print(f"distance= {avgDistance[-1]}")
            time.sleep(1)

            if (avgDistance[-1]-avgDistance[-2] > 4):
                arduino.play_tone(tonePin, 1500, 500)
                
            else: 
                pass

        except KeyboardInterrupt:
            system_menu()

def seven_seg_SR(toDisplay,option="decimal"):
    """
    seven_seg_SR function is used to initiate the Shift Register for the 7-segment-display
    Inputs:
        :param toDisplay: single digit number you want to display to a digit
        :param option: decimal point or not
    Return: 
        None
        
    """
    if option=="decimal":
        # making the decimal point show
        alphaNumericCode[toDisplay][7]=1
        pass

    else:
        pass
    # displaying the number entered as paramater "toDisplay" on seven seg 
    for i in reversed(range(len(alphaNumericCode[toDisplay]))):
        arduino.digital_write(SER,alphaNumericCode[toDisplay][i])
        arduino.digital_write(SRCLK,1)
        arduino.digital_write(SRCLK,0)
    arduino.digital_write(RCLK,1)
    arduino.digital_write(RCLK,0)

    # turning of decimal point so it doesn't show for consequent digits when not wanted
    alphaNumericCode[toDisplay][7]=0

def turn_digits_off():
    """
    turn_digits_off function is used to turn all digits off on the 7-segment-display
    
    Inputs: 
        None
    Return: 
        None
    """
    arduino.digital_write(firstDigitPin,1)
    arduino.digital_write(secondDigitPin,1)
    arduino.digital_write(thirdDigitPin,1)
    arduino.digital_write(fourthDigitPin,1)

def turn_digit1_on():
    """
    turns only first digit of seven seg on, switches off the rest

    Inputs: 
        None
    Return: 
        None
    """
    arduino.digital_write(7,0)
    arduino.digital_write(6,1)
    arduino.digital_write(5,1)
    arduino.digital_write(4,1)
def turn_digit2_on():
    """
    turns only second digit of seven seg on, switches off the rest

    Inputs: 
        None
    Return: 
        None
    """
    arduino.digital_write(7,1)
    arduino.digital_write(6,0)
    arduino.digital_write(5,1)
    arduino.digital_write(4,1)
def turn_digit3_on():
    """
    turns only third digit of seven seg on, switches off the rest

    Inputs: 
        None
    Return: 
        None
    """
    arduino.digital_write(7,1)
    arduino.digital_write(6,1)
    arduino.digital_write(5,0)
    arduino.digital_write(4,1)
def turn_digit4_on():
    """
    turns only fourth digit of seven seg on, switches off the rest

    Inputs: 
        None
    Return: 
        None
    """
    arduino.digital_write(7,1)
    arduino.digital_write(6,1)
    arduino.digital_write(5,1)
    arduino.digital_write(4,0)

def SRCLEAR_mimic():
    """
    SRCLEAR_mimic fucnction clears the shift register of the 7-segment-display by sending it 8 "0"s, clearing its output signals to 0V
    Inputs: 
        None 
    Return:
        None
    """
    a=0
    arduino.digital_write(SER,0)
    while a<8:
        
        arduino.digital_write(SRCLK,1)
        arduino.digital_write(SRCLK,0)
        a+=1
        time.sleep(0.0001)

    arduino.digital_write(RCLK,1)
    arduino.digital_write(RCLK,0)
        
def run_seven_seg(display):
    '''
    run_seven_seg function displays the single number onto the 7-segment display 
    Inputs:
        :param display: enter a 4 digit alphanumetic phrase
    Return: 
        None
    '''
    # intialising all digits off
    for i in range(len(sevenSegDigits)):
        arduino.digital_write(sevenSegDigits[i],1)
    
    # turning paramater display into a list
    digits = list(display)

    # infinite loop i.e displaying numbers/letters
    while True:
        try:
            
            # displaying the 1st digit 
            seven_seg_SR(digits[0],"no decimal")
            time.sleep(0.0000001)
            arduino.digital_write(firstDigitPin,0)
            arduino.digital_write(secondDigitPin,1)
            arduino.digital_write(thirdDigitPin,1)
            arduino.digital_write(fourthDigitPin,1)
            time.sleep(0.0000001)

            turn_digits_off()
            time.sleep(0.0000001)

            # displaying the 2nd digit
            seven_seg_SR(digits[1],"decimal")
            time.sleep(0.0000001)
            arduino.digital_write(firstDigitPin,1)
            arduino.digital_write(secondDigitPin,0)
            arduino.digital_write(thirdDigitPin,1)
            arduino.digital_write(fourthDigitPin,1)
            time.sleep(0.0000001)

            turn_digits_off()

            
            # displaying the 3rd digit
            seven_seg_SR(digits[2],"no decimal")
            time.sleep(0.0000001)
            arduino.digital_write(firstDigitPin,1)
            arduino.digital_write(secondDigitPin,1)
            arduino.digital_write(thirdDigitPin,0)
            arduino.digital_write(fourthDigitPin,1)
            time.sleep(0.0000001)

            turn_digits_off()

            time.sleep(0.0000001)

            # displaying the 4th digit
            seven_seg_SR(digits[3],"no decimal")
            time.sleep(0.0000001)
            arduino.digital_write(firstDigitPin,1)
            arduino.digital_write(secondDigitPin,1)
            arduino.digital_write(thirdDigitPin,1)
            arduino.digital_write(fourthDigitPin,0)
            time.sleep(0.0000001)

            turn_digits_off()

            time.sleep(0.000001)

        except KeyboardInterrupt:
            break
    time.sleep(0.01)
    # clearing the shift register
    turn_digits_off()
    SRCLEAR_mimic()

def run_seven_seg_scroll(display, speed, duration):
    '''
    run_seven_seg_scroll function scrolls through the digits of paramater "display" on the 7-segment display
    Inputs:
        :param display: enter a 4 digit alphanumeric phrase
        :param speed: "speed" of scrolling in seconds, i.e. 1s faster than 2s
        :param duration: how long this function runs for
    Return:
        None
    '''
    # intialising all digits off
    for i in range(len(sevenSegDigits)):
        arduino.digital_write(sevenSegDigits[i],1)
    
    # turning paramater "display" into a list
    digits = list(display)
    digits.append("-")

    functionStartTime = time.time()
    startTime  = time.time()

    # infinite loop i.e displaying numbers/letters
    while time.time()-functionStartTime < duration:
        try:
            while time.time()-startTime < speed:
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
            system_menu()

def seven_seg_display():
    """
    seven_seg_display function displays the last recorded temperature
    Inputs: 
        None
    Return:
        None
    """
    global temperatureData
    variable=str(round(temperatureData[-1],2))
    a,b=variable.split(".")
    if len(a)!=2:
        a="0"+b
    if len(b)!=2:
        b=b+"0"    
    print("")
    print("last recorded temperature of the room is being displayed...") #text to display the last temp
    run_seven_seg(a+b)
    system_menu()#return back to system menu


def reset_sr_LEDs():
    """
    reset_sr_LEDs function is used to clear the shift register of the LED circuit by sending it 8 "0"s, clearing its output signals to 0V
    Inputs:
        none 
    Return:
        none     
    """
    #send 8 zeros to the SR
    for _ in range(8):
        arduino.digital_write(SERLED, 0)
        arduino.digital_write(SRCLKLED, 1)
        time.sleep(0.000001)
        arduino.digital_write(SRCLKLED, 0)
    time.sleep(0.000001)
    #output those 8 zeros
    arduino.digital_write(RCLKLED, 1)
    time.sleep(0.000001)
    arduino.digital_write(RCLKLED, 0)
    time.sleep(0.000001)



def display_temperature_leds(temp):
    """
    display_temperature_leds function is used to display the inside room temperature on 8 LEDs as a temperature gauge 
    Inputs:
        :param temp: the temperature value to be displayed on the LEDs
    Return:
        none
    """

    temp = int(temp)
   # Define temperature ranges and corresponding LED patterns
    MinMaxLED = [
        (0, 12, "00000001"),  # 1 LED for temperature range 0-13
        (13, 15, "00000011"),  # 2 LEDs for temperature range 14-15
        (16, 18, "00000111"),  # 3 LEDs for temperature range 16-18
        (19, 21, "00001111"),  # 4 LEDs for temperature range 19-21
        (22, 24, "00011111"),  # 5 LEDs for temperature range 22-24
        (25, 27, "00111111"),  # 6 LEDs for temperature range 25-27
        (28, 30, "01111111"),  # 7 LEDs for temperature range 28-30
        (31, 100, "11111111")  # 8 LEDs for temperature range 31 and above
    ]

    for rangeMin, rangeMax, pattern in MinMaxLED:
        if rangeMin <= temp <= rangeMax:
            # Shift out each bit in the data string
            for bit in pattern:
                arduino.digital_write(SERLED, int(bit))
                arduino.digital_write(SRCLKLED, 1)
                time.sleep(0.0000001)
                arduino.digital_write(SRCLKLED, 0)
            # output the data onto the storage register
            arduino.digital_write(RCLKLED, 1)
            time.sleep(0.000001)
            arduino.digital_write(RCLKLED, 0)
            break

# Inputs
def thermistors():
    """
    thermistors function is used to obtain the temperature data from the thermistor and calculate the average temperature (data filteration process)
    Inputs:
        None 
    Return: 
        None
    """
    global temperatureData
    
    # test runs/calibrating thermistor

    arduino.analog_read(thermistorPin)

    read1=arduino.analog_read(thermistorPin)
    time.sleep(0.5)
    read2=arduino.analog_read(thermistorPin)
    time.sleep(0.5)
    read3=arduino.analog_read(thermistorPin)
    time.sleep(0.5)
   
    averageRead=(read1[0]+read2[0]+read3[0])/3+0.0001 # to ensure denominator in next line is never 0
    averageTemp=-21.21*math.log((10*((1024/averageRead)-1)))+72.203
    calibrationFactor=1.8

    temperatureData.append(averageTemp+calibrationFactor)

    print(f"Temperature recorded: {temperatureData[-1]} degrees celsius")
    time.sleep(0.1)

    if (temperatureData[-1] - temperatureData[-2] > 1.5):
        arduino.play_tone(tonePin, 1000, 500)
        time.sleep(0.2)
        arduino.play_tone(tonePin, 1200, 500)
        time.sleep(0.2)
        arduino.play_tone(tonePin, 1400, 500)
        time.sleep(0.2)
        print("Temperature has increased by more than 2 degrees")
    
    elif (temperatureData[-1] - temperatureData[-2] < -1.5):
        arduino.play_tone(tonePin, 900, 500)
        time.sleep(0.2)
        arduino.play_tone(tonePin, 600, 500)
        time.sleep(0.2)
        arduino.play_tone(tonePin, 400, 500)
        time.sleep(0.2)
        print("Temperature has increased by more than 2 degrees")

    elif (-1.5 < temperatureData[-1]-temperatureData[-2] < 1.5):
        return None


def secondthermistor():
    """
    secondthermistor function is used to obtain the outside room temperature from the second thermistor, and return the multiplier value to be used in the fan function
    Inputs: 
        None
    Return:
        multiplier: float value to be used in the fan function to control the fan speed 
    """
    global multiplier
    global temperatureData
    # test runs/calibrating thermistor
    arduino.analog_read(thermistorPin2)
    read4=arduino.analog_read(thermistorPin2)
    time.sleep(0.1)
    read5=arduino.analog_read(thermistorPin2)
    time.sleep(0.1)
    read6=arduino.analog_read(thermistorPin2)
    time.sleep(0.1)
    #complete the averaging calculations
    secondaverageRead=(read4[0]+read5[0]+read6[0])/3+0.0001 # to ensure denominator is never 0
    secondaverageTemp=-21.21*math.log((10*((1024/secondaverageRead)-1)))+72.203
    calibrationFactor=1.8
    secondtemperatureData.append(secondaverageTemp+calibrationFactor)
    #print the most recent outside temperature

    print(f"Outside Temperature recorded: {secondtemperatureData[-1]} degrees celsius")
    time.sleep(0.1)

    #logic for the multiplier return, based on the difference between the inside and outside temperatures
    if (temperatureData[-1] - secondtemperatureData[-1])>0: #this is when inside is greater than outside
        if 0< (temperatureData[-1] - secondtemperatureData[-1])<1:
            multiplier = 1
            return multiplier
        elif 1<= (temperatureData[-1] - secondtemperatureData[-1]) <= 2:
            multiplier = 1.1
            return multiplier
        elif 2 < (temperatureData[-1] - secondtemperatureData[-1])<= 4 :
            multiplier = 1.2
            return multiplier
        elif 4 < (temperatureData[-1] - secondtemperatureData[-1]):
            multiplier = 1.3
            return multiplier
    
    
    if (secondtemperatureData[-1] - temperatureData[-1])>0: #this is when outside is greater than inside temperature

        if 0< (secondtemperatureData[-1] - temperatureData[-1])< 1:
            multiplier = 1
            return multiplier
        elif 1<= (secondtemperatureData[-1] - temperatureData[-1])<=2:
            multiplier = 1.1
            return multiplier
        elif 2<(secondtemperatureData[-1] - temperatureData[-1])<=4:
            multiplier = 1.2
            return multiplier
        elif 4< (secondtemperatureData[-1] - temperatureData[-1]):
            multiplier = 1.3
            return multiplier
    else:
        return None

# This is the main menu. You can choose 3 modes/options

def system_menu():
    """
    system_menu function is used to display the 3 system menu options / modes to the user
    Inputs: 
        None
    Return:
        None
    """
    turn_digits_off()
    # Display menu
    print("System Menu")
    print("-------------------------")
    print("1: Fan operation")
    print("2: Data observation")
    print ("3: Object detection mode")
    print("0: System settings")
    # Variable to hold choice (starting value is invalid)
    choice = -1 
    # Wait for input
    while True:
        try:
            choice = int(input("Option: "))
            if choice in [0, 1, 2, 3]:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")
    # Process choice
    if choice == 1:
        fan_operation()
    elif choice == 2:
        data_observation()
    elif choice == 3:
        safety_interlock()
    elif choice == 0:
        system_settings()

# This is option 1, main polling loop

def fan_operation():
    """
    fan_operation functions runs a polling loop of temperature data obtained from the thermistor which is then fed into other components of the HVAC System
    Inputs:
        None 
    Return: 
        None
    """
    global temperatureData
    global fanEnablePin
    global fan1
    global fan2
    print("")
    print("Press ctrl-c to exit loop")
    # polling loop
    while True:
            startTime=time.time()
            try:
                
                thermistors()
                secondthermistor()
                display_temperature_leds(temperatureData[-1])
                fans(temperatureData[-1])
        
                time.sleep(2.1)
                endTime=time.time()
                elapsedTime=int(endTime-startTime)
                print(f"Time taken for this cycle to be complete: {elapsedTime} seconds")
                print("")
                time.sleep(1)
               

            except KeyboardInterrupt:
                arduino.pwm_write(fanEnablePin,0)
                arduino.digital_write(fan1,0)
                arduino.digital_write(fan2,0)
                reset_sr_LEDs()
                system_menu()

# This is option 2, allows users to see data in different forms
def data_observation():
    """
    data_observation function allows the user to view the data obtained by the system through a visual representation 
    Inputs:
        None 
    Return: 
        None
    """
    print("")
    print("Data observation")
    print("-------------------------")
    print("1: Graphing function")
    print("2: Seven-segment display")
    print("0: Back to system menu")
    # Variable to hold choice (starting value is invalid)
    choice = -1 
    # Wait for input
    while True:
        try:
            choice = int(input("Option: "))
            if choice in [0, 1, 2]:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")
    # Process choice
    if choice == 1:
        print ("Select a graph")
        print("-------------------------")
        print("1: Safety Interlock graph")
        print("2: Temperature vs time graph")
        print("3: Temperature vs resistance graph")
        print("0: Back to system menu")
        while True:
            choice = -1 
            try:
                choice = int(input("Option: "))
                if choice in  [0, 1, 2, 3]:
                    break
                else:
                    print("Error: Invalid option")
            except ValueError:
                print("Error: Only numbers are accepted")
        if choice == 1:
            distance_time_graph()
        elif choice == 2:
            temperature_time_graph()
        elif choice == 3:
            temperature_resistance_graph()
        elif choice == 0:
            system_menu()
    elif choice == 2:
        seven_seg_display()
    elif choice == 0:
        system_menu()

# This is option 0, allows users to modify parameters
def system_settings():
    """
    system_settings function grants authorised users access to modifying the parameters by validating them through a security system using PIN code 
    Inputs:
        None 
    Return: 
        None
    """
    global correctPin
    print("")
    while True:
        # Asking user for pin to access system settings
        
        try:
            pin = int(input("Enter pin: ")) 
            break
        except ValueError:
            print("Error: Only numbers are accepted")

    attempt = 1
    while attempt < 3:
        if pin == correctPin:
            break
        else:
            print(f"Incorrect pin. You have {3 - attempt} attempt(s) remaining")
            while True:
                try:
                    pin = int(input("Enter pin: "))
                    attempt += 1
                    break
                except ValueError:
                    print("Error: Only numbers are accepted")
    #the while loop for the incorrect pin logic that pauses the system for 60 seconds
    while not pin == correctPin:
        
        try:
            print("Incorrect pin. Try again in 2 minutes")
            time.sleep(60)
            print("")
            print("1 min remaining")
            time.sleep(60)
            system_settings()  

        except KeyboardInterrupt:
            pass

    else:
        pass

    print("")
    print("System settings")
    print("-------------------------")
    print("1: Change pin")
    print("2: Change temperature range")
    print("0: Back to system menu")
    # Variable to hold choice (starting value is invalid)
    choice = -1 
    # Wait for input
    while True:
        try:
            choice = int(input("Option: "))
            if choice in [0, 1, 2]:
                break
            else:
                print("Error: Invalid option")
        except ValueError:
            print("Error: Only numbers are accepted")
    # Process choice
    if choice == 1:
        change_pin()
    elif choice == 2:
        change_temperature_range()
    elif choice == 0:
        print("")
        system_menu()
 
def change_pin():
    """
    change_pin function grants authorised users the ability to change the security pin required to access the system 
    Inputs:
        None 
    Return: 
        None
    """ 
    global correctPin
    # Setting a new pin
    print("")
    print("Current correct pin: " + str(correctPin))
    while True:
        try:
            correctPin = str(int(input("Enter new value for correct pin: ")))
            
            if not len(correctPin) == 4:
                print("Error: Invalid input. Enter a 4 digit number")
            else:
                correctPin = int(correctPin)
                break

        except ValueError:
            print("Error: Invalid pin value. Please enter a 4 digit number")

    
            
    print("Correct pin updated to: " + str(correctPin))
    print("")
    time.sleep(1)
    system_menu() # Making this loop back to the system menu

# Paramater 2
def change_temperature_range():
    """
    change_temperature_range function grants authorised users the ability to change the desired temperature range for the HVAC system
    Inputs:
        None 
    Return: 
        None
    """
    global desiredTemperatureRange
    # Setting a new temperature range
    print("")
    print(f"Current temperature range (degrees celsius): {desiredTemperatureRange} ")
    while True:
        try:
            desiredTemperatureRange[0] = int(input("Enter new minimum temperature (degrees celsius): "))
            desiredTemperatureRange[1] = int(input("Enter new maximum temperature (degrees celsius): "))
        
            # make sure min. temp is < max. temp
            if desiredTemperatureRange[1]-desiredTemperatureRange[0]>0:
                pass
            else:
                raise ValueError
            
            break
        except ValueError:
                print("Error: Invalid temperature range. Please enter an integer and ensure that max temp>min temp.")
    

    print ("")
    print(f"New temperature range: {desiredTemperatureRange}")
    time.sleep(1)
    print("")
    system_menu() # Making this loop back to the system menu

# This returns a random integer between 0-40      
def random_number_generator():
    """
    random_number_generator functions generates a random number to two decimal places between the integers 0 and 40
    Inputs:
        None 
    Return: 
        None
    """
    randomNumber=round(random.uniform(0,40),2) #random number logic used to find a random number 
    global temperatureData
    temperatureData.append(randomNumber)
    print(f"Inside temperature recorded: {randomNumber} degrees celsius")

# Displays graph of temperature data over the last 20 secs
def temperature_time_graph():
    """
    graphing_function graphs the temperature data obtaiend by the thermistor over the last 20 seconds
    Inputs:
        None 
    Return: 
        None
    """
    global temperatureData
    # run_seven_seg_scroll("IMAGES",1,8)

    # This is in twos since each cycle of polling loop takes 2 seconds,
    # so for every 2 seconds there will be 1 new temperature data collected

    lastTwentySeconds=[2,4,6,8,10,12,14,16,18,20]
    plt.plot(lastTwentySeconds,temperatureData[-10:])
    plt.ylabel("Temperature (C)")
    plt.xlabel("Time elapsed (s)")
    plt.title("Temperature data over last 20 sec")

    print("Would you like to save this graph, 1 = yes, 2 = no")
    v = int(input("Selection:"))
    if (v == 1):
        title = input("Please enter a name for the graph:")
        plt.savefig(f'{title}.png')
        plt.show()
        system_menu()
    elif (v == 2):
        plt.show()
        system_menu()
    elif (v !=1 and v != 2):
        system_menu()

def distance_time_graph():
    """
    distance_time_graph plots the graph of distance and time over the last 20 seconds
    Inputs: 
        None
    Return: 
        None
    """
    global avgDistance
    run_seven_seg_scroll("IMAGES",1,8)
    lastTwentySeconds = [2,4,6,8,10,12,14,16,18,20]
    #begin plotting the graph
    plt.plot(lastTwentySeconds, avgDistance[-10:])
    #include all the labels to the graph to properlly format it 
    plt.ylabel("Safety Interlock Distance")
    plt.xlabel("Time elapsed (s)")
    plt.title("Distance over last 20 sec")
    print("Would you like to save this graph, 1 = yes, 2 = no")
    v = int(input("Selection:"))

    #the different selections depending on what user wants to do and if they want to save the graph 
    if (v == 1):
        title = input("Please enter a name for the graph:")
        plt.savefig(f'{title}.png')
        plt.show()
        system_menu()
    elif (v == 2):
        plt.show()
        system_menu()
    elif (v !=1 and v != 2):
        system_menu()

def temperature_resistance_graph():
    """
    temeperature_resistance_graph plots the graph of temperature and resistance over the last 20 seconds
    Inputs: 
        None
    Return: 
        None
    """
    global temperatureData
    global avgResistance
    
    # This is in twos since each cycle of polling loop takes 2 seconds,
    # so for every 2 seconds there will be 1 new temperature data collected
    run_seven_seg_scroll("IMAGES",1,8)

    plt.plot(avgResistance[-10:],temperatureData[-10:])
    plt.ylabel("Temperature (C)")
    plt.xlabel("Resistance (A)")
    plt.title("Temperature data againt Resistance")

    print("Would you like to save this graph, 1 = yes, 2 = no")
    v = int(input("Selection:"))
    if (v == 1):
        title = input("Please enter a name for the graph:")
        plt.savefig(f'{title}.png')
        plt.show()
        system_menu()
    elif (v == 2):
        plt.show()
        system_menu()
    elif (v !=1 and v != 2):
        system_menu()

def fans(tempReading):
    """
    fans function is used to operate the fan and control its speed based on the temperature values obtained by the thermistors
    Inputs:
        :param tempReading (integer): the most recent temperature value obtained by the thermistor  
    Return: 
        None
    """
    #begin by taking in the global values of the temp range and multiplier variables
    global desiredTemperatureRange
    global multiplier
    if tempReading < desiredTemperatureRange[0]:
        if tempReading <= (desiredTemperatureRange[0] / 5):
            arduino.pwm_write(fanEnablePin, 255)
            arduino.digital_pin_write(fan1, 1)
            arduino.digital_pin_write(fan2, 0)
            print("")
            print("Turned Heater On - Running at speed 5!")
        elif (desiredTemperatureRange[0] / 5) < tempReading <= (desiredTemperatureRange[0] / 4):
            arduino.pwm_write(fanEnablePin, 196*multiplier)#include the * multiplier logic to make sure that the multiplier has control over the fan speed
            arduino.digital_pin_write(fan1, 1)
            arduino.digital_pin_write(fan2, 0)
            print("")
            print("Turned Heater On - Running at speed 4!")
        elif (desiredTemperatureRange[0] / 4) < tempReading <= (desiredTemperatureRange[0] / 2):
            arduino.pwm_write(fanEnablePin, 171*multiplier)
            arduino.digital_pin_write(fan1, 1)
            arduino.digital_pin_write(fan2, 0)
            print("")
            print("Turned Heater On - Running at speed 3!")
        elif (desiredTemperatureRange[0] / 2) < tempReading <= (3*(desiredTemperatureRange[0]/4)): 
            arduino.pwm_write(fanEnablePin, 145*multiplier)
            arduino.digital_pin_write(fan1, 1)
            arduino.digital_pin_write(fan2, 0)
            print("")
            print("Turned Heater On - Running at speed 2!")
        elif (3*(desiredTemperatureRange[0] / 4)) < tempReading < (desiredTemperatureRange[0]):
            arduino.pwm_write(fanEnablePin, 119*multiplier)
            arduino.digital_pin_write(fan1, 1)
            arduino.digital_pin_write(fan2, 0)
            print("")
            print("Turned Heater On - Running at speed 1!")#final condition for the Fan control function that ensures that 5 distinct temperature ranges are set D

    # Changes the speed of the cooling fan based on how far away the temperature is from the desired temperature range
    elif tempReading > desiredTemperatureRange[1]:
        if tempReading >= (2*desiredTemperatureRange[1]):
            arduino.pwm_write(fanEnablePin, 255)
            arduino.digital_pin_write(fan1, 0)
            arduino.digital_pin_write(fan2, 1)
            print("")
            print("Turned Cooler On - Running at speed 5!")
        elif (1.75*desiredTemperatureRange[1]) <= tempReading < (2*desiredTemperatureRange[1]):
            arduino.pwm_write(fanEnablePin,196*multiplier)
            arduino.digital_pin_write(fan1, 0)
            arduino.digital_pin_write(fan2, 1)
            print("")
            print("Turned Cooler On - Running at speed 4!")
        elif (1.5*desiredTemperatureRange[1]) <= tempReading < (1.75*desiredTemperatureRange[1]):
            arduino.pwm_write(fanEnablePin,171*multiplier)
            arduino.digital_pin_write(fan1, 0)
            arduino.digital_pin_write(fan2, 1)
            print("")
            print("Turned Cooler On - Running at speed 3!")
        elif (1.25*desiredTemperatureRange[1]) <= tempReading < (1.5*desiredTemperatureRange[1]): 
            arduino.pwm_write(fanEnablePin, 145*multiplier)
            arduino.digital_pin_write(fan1, 0)
            arduino.digital_pin_write(fan2, 1)
            print("")
            print("Turned Cooler On - Running at speed 2!")
        elif desiredTemperatureRange[1] < tempReading < (1.25*desiredTemperatureRange[1]):
            arduino.pwm_write(fanEnablePin, 119*multiplier)
            arduino.digital_pin_write(fan1, 0)
            arduino.digital_pin_write(fan2, 1)
            print("")
            print("Turned Cooler On - Running at speed 1!")

    # Turns fan off when the temperature obtained by the thermistor is within the desired temperature range 
    elif desiredTemperatureRange[0] <= tempReading <= desiredTemperatureRange[1]:
        arduino.digital_pin_write(fan1, 0)
        arduino.digital_pin_write(fan2, 0)
        print("")
        print("Fan Turned Off!")

    time.sleep(5)

system_menu()