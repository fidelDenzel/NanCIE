import smbus					#import SMBus module of I2C
import math
import time         #import
import statistics as stat

bus = smbus.SMBus(1)
Device_Address = 0x00

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_init(slaveAddr = 0x69):
	global Device_Address

	Device_Address = slaveAddr

	#write to sample rate register
	bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
	
	#Write to power management register
	bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
	
	#Write to Configuration register
	bus.write_byte_data(Device_Address, CONFIG, 0)
	
	#Write to Gyro configuration register
	bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
	
	#Write to interrupt enable register
	bus.write_byte_data(Device_Address, INT_ENABLE, 1)

def read_raw_data(addr):
	global Device_Address
	#Accelero and Gyro value are 16-bit
	high = bus.read_byte_data(Device_Address, addr)
	low = bus.read_byte_data(Device_Address, addr+1)

	#concatenate higher and lower value
	value = ((high << 8) | low)
	
	#to get signed value from mpu6050
	if(value > 32768):
			value = value - 65536
	return value

# Function to calibrate the MPU6050
def calibrate_mpu6050(num_samples=1000):
    print("Calibrating MPU6050... Please ensure the device is stationary.")
    accel_offsets = {'x':0, 'y':0, 'z':0}
    gyro_offsets = {'x':0, 'y':0, 'z':0}
    
    for _ in range(num_samples):
        # Read raw accelerometer data
        acc_x = read_raw_data(0x3B)
        acc_y = read_raw_data(0x3D)
        acc_z = read_raw_data(0x3F)
        
        # Read raw gyroscope data
        gyro_x = read_raw_data(0x43)
        gyro_y = read_raw_data(0x45)
        gyro_z = read_raw_data(0x47)
        
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

def complementary_filter(gyro_value, accel_value, dt, alpha = 0.98, value = 0.0):
	
	value += gyro_value * dt
	value = alpha * value + (1 - alpha) * accel_value

	return value

# Function to calculate accelerometer angles
def get_accel_angle(acc_x, acc_y, acc_z):
	roll = 0
	pitch = 0
    # Calculate roll and pitch from accelerometer data
	if (acc_x == 0 or acc_y == 0 or acc_z == 0):
		roll = 0
		pitch = 0
	else:
		roll = math.atan2(acc_y, acc_z) * 180 / math.pi
		pitch = math.atan(-acc_x / math.sqrt(acc_y * acc_y + acc_z * acc_z)) * 180 / math.pi
	return roll, pitch

def roll_pitch_calibration(num_sample):
	accel_offsets = {'x':0, 'y':0, 'z':0}
	gyro_offsets = {'x':0, 'y':0, 'z':0}
	roll_offsets = []
	pitch_offsets = []

	dt = 0.08
	num_samples = 1000
	
	for _ in range(num_samples):
		# Read raw accelerometer data
		acc_x = read_raw_data(0x3B)
		acc_y = read_raw_data(0x3D)
		acc_z = read_raw_data(0x3F)
		
		# Read raw gyroscope data
		gyro_x = read_raw_data(0x43)
		gyro_y = read_raw_data(0x45)
		gyro_z = read_raw_data(0x47)

		# Convert gyroscope data to degrees per second
		gyro_x = gyro_x / 131.0
		gyro_y = gyro_y / 131.0
		gyro_z = gyro_z / 131.0

		accel_offsets['x'] += acc_x
		accel_offsets['y'] += acc_y
		accel_offsets['z'] += acc_z
		
		gyro_offsets['x'] += gyro_x
		gyro_offsets['y'] += gyro_y
		gyro_offsets['z'] += gyro_z
		
		# Calculate accelerometer angles
		accel_roll, accel_pitch = get_accel_angle(acc_x, acc_y, acc_z)

		roll_th = complementary_filter(gyro_value=gyro_x,accel_value=accel_roll,dt=dt)
		pitch_th = complementary_filter(gyro_value=gyro_y,accel_value=accel_pitch,dt=dt)
		# print(f"Roll Offsets: {roll_th}")
		# print(f"Pitch Offsets: {pitch_th}")
		roll_offsets.append(roll_th)
		pitch_offsets.append(pitch_th)
		
		time.sleep(0.001)  # 1ms delay between samples
	
	# Compute average offsets
	accel_offsets = {k: v / num_samples for k, v in accel_offsets.items()}
	gyro_offsets = {k: v / num_samples for k, v in gyro_offsets.items()}
	roll_offset = stat.mean(roll_offsets)
	pitch_offset = stat.mean(pitch_offsets)

	print("Calibration complete.")
	print(f"Accelerometer Offsets: {accel_offsets}")
	print(f"Gyroscope Offsets: {gyro_offsets}")
	
	return roll_offset, pitch_offset