import smbus
import time
import math

# MPU6050 Registers and Addresses
MPU6050_ADDR = 0x68  # I2C address of the MPU6050

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
ACCEL_CONFIG = 0x1C
INT_ENABLE = 0x38

# Function to initialize the MPU6050
def MPU_Init(bus):
    # Wake up the MPU-6050 since it starts in sleep mode
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0x00)
    time.sleep(0.1)
    
    # Set sample rate to 1kHz by writing SMPLRT_DIV register
    bus.write_byte_data(MPU6050_ADDR, SMPLRT_DIV, 0x07)
    
    # Set accelerometer configuration to ±2g
    bus.write_byte_data(MPU6050_ADDR, ACCEL_CONFIG, 0x00)
    
    # Set gyroscope configuration to ±250 degrees/s
    bus.write_byte_data(MPU6050_ADDR, GYRO_CONFIG, 0x00)
    
    # Configure the interrupt (optional)
    bus.write_byte_data(MPU6050_ADDR, INT_ENABLE, 0x01)
    time.sleep(0.1)

# Function to read raw data from the MPU6050
def read_raw_data(bus, addr):
    # Read two bytes of data starting from the given address
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    
    # Combine high and low bytes
    value = (high << 8) | low
    
    # Convert to signed integer
    if value > 32768:
        value = value - 65536
    return value

# Function to calibrate the MPU6050
def calibrate_mpu6050(bus, num_samples=1000):
    print("Calibrating MPU6050... Please ensure the device is stationary.")
    accel_offsets = {'x':0, 'y':0, 'z':0}
    gyro_offsets = {'x':0, 'y':0, 'z':0}
    
    for _ in range(num_samples):
        # Read raw accelerometer data
        acc_x = read_raw_data(bus, 0x3B)
        acc_y = read_raw_data(bus, 0x3D)
        acc_z = read_raw_data(bus, 0x3F)
        
        # Read raw gyroscope data
        gyro_x = read_raw_data(bus, 0x43)
        gyro_y = read_raw_data(bus, 0x45)
        gyro_z = read_raw_data(bus, 0x47)
        
        accel_offsets['x'] += acc_x
        accel_offsets['y'] += acc_y
        accel_offsets['z'] += acc_z
        
        gyro_offsets['x'] += gyro_x
        gyro_offsets['y'] += gyro_y
        gyro_offsets['z'] += gyro_z
        
        time.sleep(0.001)  # 1ms delay between samples
    
    # Compute average offsets
    accel_offsets = {k: v / num_samples for k, v in accel_offsets.items()}
    gyro_offsets = {k: v / num_samples for k, v in gyro_offsets.items()}
    
    print("Calibration complete.")
    print(f"Accelerometer Offsets: {accel_offsets}")
    print(f"Gyroscope Offsets: {gyro_offsets}")
    
    return accel_offsets, gyro_offsets

# Function to calculate accelerometer angles
def get_accel_angle(acc_x, acc_y, acc_z):
    # Calculate roll and pitch from accelerometer data
    roll = math.atan2(acc_y, acc_z) * 180 / math.pi
    pitch = math.atan(-acc_x / math.sqrt(acc_y * acc_y + acc_z * acc_z)) * 180 / math.pi
    return roll, pitch

# Main function
def main():
    # Initialize I2C (SMBus)
    bus = smbus.SMBus(1)  # 1 indicates /dev/i2c-1
    
    # Initialize MPU6050
    MPU_Init(bus)
    
    # Calibrate MPU6050
    accel_offsets, gyro_offsets = calibrate_mpu6050(bus, num_samples=2000)
    
    # Variables for complementary filter
    alpha = 0.98
    dt = 0.01  # Time interval in seconds (100Hz)
    roll = 0.0
    pitch = 0.0
    
    print("\nStarting sensor fusion. Press Ctrl+C to exit.\n")
    
    try:
        while True:
            start_time = time.time()
            
            # Read raw accelerometer data
            acc_x = read_raw_data(bus, 0x3B) - accel_offsets['x']
            acc_y = read_raw_data(bus, 0x3D) - accel_offsets['y']
            acc_z = read_raw_data(bus, 0x3F) - accel_offsets['z']
            
            # Read raw gyroscope data
            gyro_x = read_raw_data(bus, 0x43) - gyro_offsets['x']
            gyro_y = read_raw_data(bus, 0x45) - gyro_offsets['y']
            gyro_z = read_raw_data(bus, 0x47) - gyro_offsets['z']
            
            # Convert gyroscope data to degrees per second
            gyro_x = gyro_x / 131.0
            gyro_y = gyro_y / 131.0
            gyro_z = gyro_z / 131.0
            
            # Calculate accelerometer angles
            accel_roll, accel_pitch = get_accel_angle(acc_x, acc_y, acc_z)
            
            # Integrate gyroscope data
            roll += gyro_x * dt
            pitch += gyro_y * dt
            
            # Apply complementary filter
            roll = alpha * roll + (1 - alpha) * accel_roll
            pitch = alpha * pitch + (1 - alpha) * accel_pitch
            
            # Optional: Yaw cannot be obtained accurately without magnetometer
            # Yaw can drift over time if solely using gyroscope
            
            print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°")
            
            # Maintain loop at approximately 100Hz
            elapsed_time = time.time() - start_time
            time_to_sleep = dt - elapsed_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
    
    except KeyboardInterrupt:
        print("\nExiting...")
        pass

if __name__ == "__main__":
    main()
