import lgpio
import time

BTS7960 = lgpio.gpiochip_open(0)
FREQ = 100

movement = input("Input movement : ")

#Motor Kiri
pin_LEN = 22
pin_REN = 23
pin_LPWM = 27
pin_RPWM = 17
#Motor Kanan
pin_LEN2 = 24
pin_REN2 = 25
pin_LPWM2 = 26
pin_RPWM2 = 6

try:
    # SETUP
    #Motor Kanan
    lgpio.gpio_claim_output(BTS7960, pin_LEN)
    lgpio.gpio_claim_output(BTS7960, pin_REN)
    lgpio.gpio_claim_output(BTS7960, pin_LPWM)
    lgpio.gpio_claim_output(BTS7960, pin_RPWM)

    #Motor Kiri
    lgpio.gpio_claim_output(BTS7960, pin_LEN2)
    lgpio.gpio_claim_output(BTS7960, pin_REN2)
    lgpio.gpio_claim_output(BTS7960, pin_LPWM2)
    lgpio.gpio_claim_output(BTS7960, pin_RPWM2)

    # INITIALIZATION
    lgpio.gpio_write(BTS7960, pin_LEN,0)
    lgpio.gpio_write(BTS7960, pin_REN,0)
    lgpio.gpio_write(BTS7960, pin_LPWM,0)
    lgpio.gpio_write(BTS7960, pin_RPWM,0)

    lgpio.gpio_write(BTS7960, pin_LEN2,0)
    lgpio.gpio_write(BTS7960, pin_REN2,0)
    lgpio.gpio_write(BTS7960, pin_LPWM2,0)
    lgpio.gpio_write(BTS7960, pin_RPWM2,0)

# MAIN

    # ENABLING MOTORS
    lgpio.tx_pwm(BTS7960,pin_LPWM,100,0)
    lgpio.tx_pwm(BTS7960,pin_RPWM,200,0)

    lgpio.gpio_write(BTS7960, pin_LEN,1)
    lgpio.gpio_write(BTS7960, pin_REN,1)
    lgpio.gpio_write(BTS7960, pin_LEN2,1)
    lgpio.gpio_write(BTS7960, pin_REN2,1)

    str_part = str(movement[0])
    int_part = int(movement[1:])
    speed = float(int_part * 2 /100)

    if(int_part < 0 or int_part > 100):
        print ("Value Invalid")

    else :
        if (str_part == "R") :
            print ("Belok kanan " + str(speed) + " m/s")
            lgpio.tx_pwm(BTS7960,pin_RPWM,FREQ,int_part)
        elif (str_part == "L") :                      
            print ("Belok kiri " + str(speed) + " m/s")
            lgpio.tx_pwm(BTS7960,pin_RPWM2,FREQ,int_part)
        elif (str_part == "F") :
            print ("Maju" + str(speed) + " m/s")
            lgpio.tx_pwm(BTS7960,pin_RPWM,FREQ,int_part)
            lgpio.tx_pwm(BTS7960,pin_RPWM2,FREQ,(int_part - 1.82))
        elif (str_part == "S") :
            print ("Mundur" + str(speed) + " m/s")
            lgpio.tx_pwm(BTS7960,pin_LPWM,FREQ, int_part)
            lgpio.tx_pwm(BTS7960,pin_LPWM2,FREQ,(int_part - 1.5))


    while True:
        pass  

        
finally:
# except KeyboardInterrupt:
    print("ending\n")
    lgpio.tx_pwm(BTS7960,pin_RPWM,FREQ,0)
    lgpio.gpio_write(BTS7960, pin_LEN,0)
    lgpio.gpio_write(BTS7960, pin_REN,0)

    lgpio.tx_pwm(BTS7960,pin_RPWM2,FREQ,0)
    lgpio.gpio_write(BTS7960, pin_LEN2,0)
    lgpio.gpio_write(BTS7960, pin_REN2,0)
    
    lgpio.gpiochip_close(BTS7960)