import RPi.GPIO as pio
import time

pin_LEN = 22
pin_REN = 23
pin_LPWM = 27
pin_RPWM = 17
pio.setmode(pio.BCM)
pio.setwarnings(False)

pio.setup(pin_LEN, pio.OUT)
pio.setup(pin_REN, pio.OUT)
pio.setup(pin_LPWM, pio.OUT)
pio.setup(pin_RPWM, pio.OUT)

while True:
    x = input("Type")

    # if()
    print("left start")
    pio.output(pin_RPWM, pio.LOW)
    pio.output(pin_LPWM, pio.HIGH)
    pio.output(pin_LEN, pio.LOW)
    pio.output(pin_REN, pio.LOW)
    time.sleep(2)
    pio.output(pin_LEN, pio.LOW)
    pio.output(pin_REN, pio.LOW)
    # print("stop")
    # time.sleep(1)
    # print("RIGHT")
    # pio.output(pin_LEN, pio.LOW)
    # pio.output(pin_REN, pio.LOW)
    # pio.output(pin_RPWM, pio.LOW)
    # pio.output(pin_LPWM, pio.LOW)
    # time.sleep(3)
    # print("right start")
    # pio.output(pin_LPWM, pio.LOW)
    # pio.output(pin_RPWM, pio.HIGH)
    # pio.output(pin_LEN, pio.HIGH)
    # pio.output(pin_REN, pio.HIGH)
    # time.sleep(1)
   

    # pio.output(pin_LEN, pio.LOW)
    # time.sleep(.1)
    # pio.output(pin_REN, pio.LOW)
    # time.sleep(.1)
    
    # print("LEFT")
    # time.sleep(1)
    # pio.output(pin_LEN, pio.LOW)
    # pio.output(pin_REN, pio.LOW)
    # time.sleep(1)
    # pio.output(pin_LPWM, pio.HIGH)
    # pio.output(pin_RPWM, pio.LOW)
    # pio.output(pin_LEN, pio.HIGH)
    # pio.output(pin_REN, pio.HIGH)

    # time.sleep(1)
    # print("LEFT")
    # pio.output(pin_LEN, pio.LOW)
    # pio.output(pin_REN, pio.LOW)
    # time.sleep(1)
    # pio.output(pin_LPWM, pio.HIGH)
    # pio.output(pin_RPWM, pio.LOW)
    # pio.output(pin_LEN, pio.HIGH)
    # pio.output(pin_REN, pio.HIGH)

    # time.sleep(1)