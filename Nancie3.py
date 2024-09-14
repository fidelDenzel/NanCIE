import pygame
import lgpio
import time
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((100, 100))

# Initialize GPIO
BTS7960 = lgpio.gpiochip_open(0)
FREQ = 100
max_omega = (1/0.03) * 2*math.pi# radiant per second
wheel_r = 0.1
max_v = max_omega * wheel_r

# Motor Pins
pin_LEN = 22
pin_REN = 23
pin_LPWM = 27
pin_RPWM = 17
pin_LEN2 = 24
pin_REN2 = 26
pin_LPWM2 = 25
pin_RPWM2 = 16

# Setup GPIO
lgpio.gpio_claim_output(BTS7960, pin_LEN)
lgpio.gpio_claim_output(BTS7960, pin_REN)
lgpio.gpio_claim_output(BTS7960, pin_LPWM)
lgpio.gpio_claim_output(BTS7960, pin_RPWM)
lgpio.gpio_claim_output(BTS7960, pin_LEN2)
lgpio.gpio_claim_output(BTS7960, pin_REN2)
lgpio.gpio_claim_output(BTS7960, pin_LPWM2)
lgpio.gpio_claim_output(BTS7960, pin_RPWM2)

# Initialization
lgpio.gpio_write(BTS7960, pin_LEN, 0)
lgpio.gpio_write(BTS7960, pin_REN, 0)
lgpio.gpio_write(BTS7960, pin_LPWM, 0)
lgpio.gpio_write(BTS7960, pin_RPWM, 0)
lgpio.gpio_write(BTS7960, pin_LEN2, 0)
lgpio.gpio_write(BTS7960, pin_REN2, 0)
lgpio.gpio_write(BTS7960, pin_LPWM2, 0)
lgpio.gpio_write(BTS7960, pin_RPWM2, 0)

# Enabling Motors
lgpio.tx_pwm(BTS7960, pin_LPWM, 100, 0)
lgpio.tx_pwm(BTS7960, pin_RPWM, 200, 0)
lgpio.gpio_write(BTS7960, pin_LEN, 1)
lgpio.gpio_write(BTS7960, pin_REN, 1)
lgpio.gpio_write(BTS7960, pin_LEN2, 1)
lgpio.gpio_write(BTS7960, pin_REN2, 1)

# Initialize speed adjustments
motor1_speed_adjustment = 1.0  # Adjustment factor for Motor 1
motor2_speed_adjustment = 1.0 # Adjustment factor for Motor 2

# Function to stop the robot
def stop_robot():
    print("Stopping the robot")
    lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM2, FREQ, 0)

# Function to measure speed difference
def measure_speed_difference():
    # Placeholder function to measure speed
    # This should return the speed of each motor, e.g., using encoders
    speed_motor1 = 100  # Example reading from an encoder or other sensor
    speed_motor2 = 100  # Example reading from an encoder or other sensor
    return speed_motor1, speed_motor2

# Function to adjust motor speeds manually
def adjust_motor_speeds(target_speed):
    global motor1_speed_adjustment, motor2_speed_adjustment

    # Calculate new PWM duty cycle values
    duty_cycle_motor1 = max(0, min(100, target_speed * motor1_speed_adjustment))
    duty_cycle_motor2 = max(0, min(100, target_speed * motor2_speed_adjustment))

    # Apply new speed adjustment factors
    lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, duty_cycle_motor1)
    lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, duty_cycle_motor2)

# Function to move the robot
def move_robot(direction, speed):
    global motor1_speed_adjustment, motor2_speed_adjustment

    motor1_speed = speed * motor1_speed_adjustment
    motor2_speed = speed * motor2_speed_adjustment

    if direction == 'forward':
        print("Moving forward at", (speed/100) * max_v, "m/s")
        lgpio.t9x_pwm(BTS7960, pin_LPWM, FREQ, motor1_speed)
        lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, motor2_speed)
    elif direction == 'backward':
        print("Moving backward at", (speed/100) * max_v, "m/s")
        lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, motor1_speed)
        lgpio.tx_pwm(BTS7960, pin_LPWM2, FREQ, motor2_speed)
    elif direction == 'left':
        print("Turning left at", (speed/100) * max_v, "m/s")
        lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, motor1_speed)
    elif direction == 'right':
        print("Turning right at", (speed/100) * max_v, "m/s")
        lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, motor2_speed)
    elif direction == 'spin':
        print("360 Dance Move at", (speed/100) * max_v, "m/s")
        lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, motor2_speed) 
        lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, motor1_speed)   

# Initialize speed
current_speed = 10  # Default speed

# Main loopbbbbby
try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_robot('forward', current_speed)
                elif event.key == pygame.K_DOWN:
                    move_robot('backward', current_speed)
                elif event.key == pygame.K_LEFT:
                    move_robot('left', current_speed)
                elif event.key == pygame.K_RIGHT:
                    move_robot('right', current_speed)
                elif event.key == pygame.K_RETURN:
                    move_robot('spin', current_speed)    
                elif event.key == pygame.K_q:
                    motor1_speed_adjustment = max(0, motor1_speed_adjustment - 0.1)  # Decrease Motor 1 speed adjustment
                    print("Motor 1 speed adjustment:", motor1_speed_adjustment)
                    adjust_motor_speeds(current_speed)
                elif event.key == pygame.K_e:
                    motor1_speed_adjustment = min(2.0, motor1_speed_adjustment + 0.1)  # Increase Motor 1 speed adjustment
                    print("Motor 1 speed adjustment:", motor1_speed_adjustment)
                    adjust_motor_speeds(current_speed)
                elif event.key == pygame.K_z:
                    motor2_speed_adjustment = max(0, motor2_speed_adjustment - 0.1)  # Decrease Motor 2 speed adjustment
                    print("Motor 2 speed adjustment:", motor2_speed_adjustment)
                    adjust_motor_speeds(current_speed)
                elif event.key == pygame.K_c:
                    motor2_speed_adjustment = min(2.0, motor2_speed_adjustment + 0.1)  # Increase Motor 2 speed adjustment
                    print("Motor 2 speed adjustment:", motor2_speed_adjustment)
                    adjust_motor_speeds(current_speed)
                elif event.key == pygame.K_1:
                    current_speed = 10   # Speed level 1
                    print("Speed set to 10%")
                elif event.key == pygame.K_2:
                    current_speed = 20  # Speed level 2
                    print("Speed set to 20%")
                elif event.key == pygame.K_3:
                    current_speed = 30  # Speed level 3
                    print("Speed set to 30%")
                elif event.key == pygame.K_4:
                    current_speed = 40  # Speed level 4
                    print("Speed set to 40%")    
                elif event.key == pygame.K_5:
                    current_speed = 50   # Speed level 5
                    print("Speed set to 50%")
                elif event.key == pygame.K_6:
                    current_speed = 60  # Speed level 6
                    print("Speed set to 60%")
                elif event.key == pygame.K_7:
                    current_speed = 70  # Speed level 7
                    print("Speed set to 70%")
                elif event.key == pygame.K_8:
                    current_speed = 80  # Speed level 8
                    print("Speed set to 80") 
                elif event.key == pygame.K_9:
                    current_speed = 90  # Speed level 9
                    print("Speed set to 90%")
                elif event.key == pygame.K_0:
                    current_speed = 100  # Speed level 10
                    print("Speed set to 100") 
            elif event.type == pygame.KEYUP:
                stop_robot()

        time.sleep(0.1)  # To avoid high CPU usage

finally:
    print("Ending\n")
    stop_robot()
    lgpio.gpio_write(BTS7960, pin_LEN, 0)
    lgpio.gpio_write(BTS7960, pin_REN, 0)
    lgpio.gpio_write(BTS7960, pin_LEN2, 0)
    lgpio.gpio_write(BTS7960, pin_REN2, 0)
    lgpio.gpiochip_close(BTS7960)
    pygame.quit()