import RPi.GPIO as pio
import time

pin_LEN = 22
pin_REN = 23
pin_LPWM = 17
pin_RPWM = 27
pio.setmode(pio.BCM)
pio.setwarnings(False)

try:
    pio.setup(pin_LEN, pio.OUT)
    pio.setup(pin_REN, pio.OUT)
    pio.setup(pin_LPWM, pio.OUT)
    pio.setup(pin_RPWM, pio.OUT)

    pio.output(pin_LEN, pio.LOW)
    pio.output(pin_REN, pio.LOW)
    pio.output(pin_LPWM, pio.LOW)
    pio.output(pin_RPWM, pio.LOW)

    motor1_Lpwm = pio.PWM(pin_LPWM, 100)
    motor1_Lpwm.start(0)

    motor1_Rpwm = pio.PWM(pin_RPWM, 200)
    motor1_Rpwm.start(0)

    pio.output(pin_REN, pio.HIGH)
    pio.output(pin_LEN, pio.HIGH)

    print("starting loop")
    time.sleep(2)

    while True:
        
        print("LPWM")
        for iter in range(100,0,-1):
            
            motor1_Lpwm.ChangeDutyCycle(iter)
            time.sleep(0.1)
        
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)
        time.sleep(1)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)

        print("RPWM")
        for iter in range(100, 0, -1):
            
            motor1_Rpwm.ChangeDutyCycle(iter)
            time.sleep(0.1)
        
        pio.output(pin_LEN, pio.LOW)
        pio.output(pin_REN, pio.LOW)
        time.sleep(1)
        pio.output(pin_LEN, pio.HIGH)
        pio.output(pin_REN, pio.HIGH)
        
except KeyboardInterrupt:
    pass

print("finishing up")

motor1_Lpwm.stop()
pio.output(pin_LEN, 0)
pio.output(pin_REN, 0)
time.sleep(1)
pio.cleanup()