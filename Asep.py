import RPi.GPIO as pio
import time

movement = input("Input movement : ")

#Motor Kanan
pin_LEN = 22
pin_REN = 23
pin_LPWM = 27
pin_RPWM = 17
#Motor Kiri
pin_LEN2 = 24
pin_REN2 = 25
pin_LPWM2 = 26
pin_RPWM2 = 16
pio.setmode(pio.BCM)
pio.setwarnings(False)

#Motor Kanan
pio.setup(pin_LEN, pio.OUT)
pio.setup(pin_REN, pio.OUT)
pio.setup(pin_LPWM, pio.OUT)
pio.setup(pin_RPWM, pio.OUT)

pio.output(pin_LEN, pio.LOW)
pio.output(pin_REN, pio.LOW)
pio.output(pin_LPWM, pio.LOW)
pio.output(pin_RPWM, pio.LOW)

#Motor Kiri
pio.setup(pin_LEN2, pio.OUT)
pio.setup(pin_REN2, pio.OUT)
pio.setup(pin_LPWM2, pio.OUT)
pio.setup(pin_RPWM2, pio.OUT)

pio.output(pin_LEN2, pio.LOW)
pio.output(pin_REN2, pio.LOW)
pio.output(pin_LPWM2, pio.LOW)
pio.output(pin_RPWM2, pio.LOW)

#Motor Kanan
motor1_Lpwm = pio.PWM(pin_LPWM, 100)
motor1_Lpwm.start(0)

motor1_Rpwm = pio.PWM(pin_RPWM, 200)
motor1_Rpwm.start(0)

pio.output(pin_REN, pio.HIGH)
pio.output(pin_LEN, pio.HIGH)

#Motor Kiri
motor2_Lpwm = pio.PWM(pin_LPWM2, 100)
motor2_Lpwm.start(0)

motor2_Rpwm = pio.PWM(pin_RPWM2, 200)
motor2_Rpwm.start(0)

pio.output(pin_REN2, pio.HIGH)
pio.output(pin_LEN2, pio.HIGH)

str_part = str(movement[0])
int_part = int(movement[1:])
speed = float(int_part * 2 /100)

if(int_part < 0 or int_part > 100):
    print ("Value Invalid")

else :
    if (str_part == "L") :
        print ("Belok kiri " + str(speed) + " m/s")
        motor1_Rpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)
      
    elif (str_part == "R") :
        print ("Kanan deh " + str(speed) + " m/s")
        motor2_Lpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)
 
    elif (str_part == "F") :
        print ("Maju hei " + str(speed) + " m/s")
        motor1_Rpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)

        motor2_Lpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN2, pio.HIGH)
        pio.output(pin_REN2, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN2, pio.LOW)
        pio.output(pin_REN2, pio.LOW)

    elif (str_part == "S") :
        print ("Mundur bapak " + str(speed) + " m/s")
        motor1_Lpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)

        motor2_Rpwm.ChangeDutyCycle(int_part)
        time.sleep(2)
        pio.output(pin_LEN2, pio.HIGH)
        pio.output(pin_REN2, pio.HIGH)
        time.sleep(1)
        pio.output(pin_LEN2, pio.LOW)
        pio.output(pin_REN2, pio.LOW)
