
import lgpio
import math


max_omega = (1/0.03) * 2 * math.pi # radiant per second
wheel_r = 0.1
max_v = 1.5 #m/s

# Motor Pins
pin_LEN = 22
# pin_REN = 
pin_LPWM = 27
pin_RPWM = 17

pin_LEN2 = 26
# pin_REN2 = 
pin_LPWM2 = 6
pin_RPWM2 = 5

# Initialize speed
current_speed = 10  # Default speed
FREQ = 5000 #0 - 8k Hz

# Initialize speed adjustments
motor1_speed_adjustment = 1  # Adjustment factor for Motor 1
motor2_speed_adjustment = 1 # Adjustment factor for Motor 2

# Initialize GPIO
BTS7960 = lgpio.gpiochip_open(0)

# Setup GPIO
lgpio.gpio_claim_output(BTS7960, pin_LEN)
# lgpio.gpio_claim_output(BTS7960, pin_REN)
lgpio.gpio_claim_output(BTS7960, pin_LPWM)
lgpio.gpio_claim_output(BTS7960, pin_RPWM)
lgpio.gpio_claim_output(BTS7960, pin_LEN2)
# lgpio.gpio_claim_output(BTS7960, pin_REN2)
lgpio.gpio_claim_output(BTS7960, pin_LPWM2)
lgpio.gpio_claim_output(BTS7960, pin_RPWM2)

# Initialization
lgpio.gpio_write(BTS7960, pin_LEN, 0)
# lgpio.gpio_write(BTS7960, pin_REN, 0)
lgpio.gpio_write(BTS7960, pin_LPWM, 0)
lgpio.gpio_write(BTS7960, pin_RPWM, 0)

lgpio.gpio_write(BTS7960, pin_LEN2, 0)
# lgpio.gpio_write(BTS7960, pin_REN2, 0)
lgpio.gpio_write(BTS7960, pin_LPWM2, 0)
lgpio.gpio_write(BTS7960, pin_RPWM2, 0)

# Enabling Motors
lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, 0)
lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, 0)
lgpio.gpio_write(BTS7960, pin_LEN, 1)
# lgpio.gpio_write(BTS7960, pin_REN, 1)

lgpio.tx_pwm(BTS7960, pin_LPWM2, FREQ, 0)
lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, 0)
lgpio.gpio_write(BTS7960, pin_LEN2, 1)
# lgpio.gpio_write(BTS7960, pin_REN2, 1)

# Function to measure speed difference
def measure_speed_difference():
    # Placeholder function to measure speed
    # This should return the speed of each motor, wwae.g., using encoders

    speed_motor1 = 100  # Example reading from an encoder or other sensor
    speed_motor2 = 100  # Example reading from an encoder or other sensor
    
    return speed_motor1, speed_motor2

# Function to adjust motor speeds manually
def adjust_motor_speeds(target_speed) :
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
        lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, motor1_speed)
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

# Function to stop the robot
def stop_robot():
    print("Stopping the robot")
    lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM2, FREQ, 0)

#Funtion to shutdown robot
def end_robot():
    print("Ending robot\n")
    lgpio.tx_pwm(BTS7960, pin_RPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_RPWM2, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM, FREQ, 0)
    lgpio.tx_pwm(BTS7960, pin_LPWM2, FREQ, 0)
    lgpio.gpio_write(BTS7960, pin_LEN, 0)
    # lgpio.gpio_write(BTS7960, pin_REN, 0)
    lgpio.gpio_write(BTS7960, pin_LEN2, 0)
    # lgpio.gpio_write(BTS7960, pin_REN2, 0)
    lgpio.gpiochip_close(BTS7960)