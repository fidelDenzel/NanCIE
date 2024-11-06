import smbus
import time
import math

# MPU6050 Registers and Address
MPU6050_ADDR = 0x69
PWR_MGMT_1 = 0x6B
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C

# Sensitivity scale factor for gyroscope (assuming ±250°/s range)
GYRO_SENSITIVITY = 131.0  # LSB/°/s

# Initialize I2C bus
bus = smbus.SMBus(1)  # For Raspberry Pi I2C bus 1

# Initialize yaw angle
yaw = 0.0

# Complementary filter constant
ALPHA = 0.98

# Function to initialize MPU6050
def MPU_Init():
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)  # Wake up the MPU-6050

def read_raw_data(addr):
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    value = (high << 8) | low
    if value > 32768:
        value = value - 65536
    return value

# Initialize MPU6050
MPU_Init()

# Timestamp for integration
prev_time = time.time()

try:
    while True:
        # Time difference for integration
        current_time = time.time()
        dt = current_time - prev_time
        prev_time = current_time

        # Read gyroscope z-axis data for yaw rate
        gyro_z = read_raw_data(0x47) / GYRO_SENSITIVITY  # degrees per second

        # Calculate yaw by integrating the gyroscope z data
        yaw += gyro_z * dt

        # Apply complementary filter to reduce drift
        yaw = ALPHA * (yaw + gyro_z * dt) + (1 - ALPHA) * yaw

        # Print yaw angle in degrees
        print(f"Yaw: {yaw:.2f}°")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nProgram interrupted.")
