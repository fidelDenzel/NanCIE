import PID
import GyrometerMPU6050 as gyNan
import MotorInterface as gyMotor

thetaPID = PID.PIDController(100,0,5)
mpu = gyNan.MPU_init(0x69)

# Main lobby
# while True:
# #Read Accelerometer raw value
# acc_x = gyNan.read_raw_data(gyNan.ACCEL_XOUT_H)/16384.0
# acc_y = gyNan.read_raw_data(gyNan.ACCEL_YOUT_H)/16384.0
# acc_z = gyNan.read_raw_data(gyNan.ACCEL_ZOUT_H)/16384.0

# #Read Gyroscope raw value
# gyro_x = gyNan.read_raw_data(gyNan.GYRO_XOUT_H)/131.0
# gyro_y = gyNan.read_raw_data(gyNan.GYRO_YOUT_H)/131.0
# gyro_z = gyNan.read_raw_data(gyNan.GYRO_ZOUT_H)/131.0

# #Full scale range +/- 250 degree/C as per sensitivity scale factor
# Ax = acc_x/16384.0
# Ay = acc_y/16384.0
# Az = acc_z/16384.0

# Gx = gyro_x/131.0
# Gy = gyro_y/131.0
# Gz = gyro_z/131.0

try:

    gyMotor.running = True
    while gyMotor.running:

        #Read Accelerometer raw value
        Ax = gyNan.read_raw_data(gyNan.ACCEL_XOUT_H)/16384.0
        Ay = gyNan.read_raw_data(gyNan.ACCEL_YOUT_H)/16384.0
        Az = gyNan.read_raw_data(gyNan.ACCEL_ZOUT_H)/16384.0

        #Read Gyroscope raw value
        Gx = gyNan.read_raw_data(gyNan.GYRO_XOUT_H)/131.0
        Gy = gyNan.read_raw_data(gyNan.GYRO_YOUT_H)/131.0
        Gz = gyNan.read_raw_data(gyNan.GYRO_ZOUT_H)/131.0

        print ("Gx=%.2f" %Gx, u'\u00b0'+ "/s", "\tGy=%.2f" %Gy, u'\u00b0'+ "/s", "\tGz=%.2f" %Gz, u'\u00b0'+ "/s", "\tAx=%.2f g" %Ax, "\tAy=%.2f g" %Ay, "\tAz=%.2f g" %Az) 	
        gyNan.time.sleep(.1)

        for event in gyMotor.pygame.event.get():
            if event.type == gyMotor.pygame.QUIT:
                running = False
            elif event.type == gyMotor.pygame.KEYDOWN:
                outp = thetaPID.compute(0, Gz)
                if outp < 0 : # if negative, robot must turn ccw
                    gyMotor.move_robot('right',outp * current_speed)  #this s because output ranges from -1 to 1 due to complex numbers vector range

                if event.key == gyMotor.pygame.K_UP:
                    gyMotor.move_robot('forward', current_speed)
                
                elif event.key == gyMotor.pygame.K_DOWN:
                    gyMotor.move_robot('backward', current_speed)
                
                elif event.key == gyMotor.pygame.K_LEFT:
                    gyMotor.move_robot('left', current_speed)
                
                elif event.key == gyMotor.pygame.K_RIGHT:
                    gyMotor.move_robot('right', current_speed)
                
                elif event.key == gyMotor.pygame.K_RETURN:
                    gyMotor.move_robot('spin', current_speed)    
                
                elif event.key >= 48 and event.key <= 57:
                    current_speed = (event.key - 48 ) * 10
                    if current_speed == 0:
                        current_speed = 100
                    print("Speed @" + str(current_speed) + " %")

            elif event.type == gyMotor.pygame.KEYUP:
                gyMotor.stop_robot()

        gyMotor.time.sleep(0.1)  # To avoid high CPU usage

finally:
    print("Ending\n")
    gyMotor.stop_robot()
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_LEN, 0)
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_REN, 0)
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_LEN2, 0)
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_REN2, 0)
    gyMotor.lgpio.gpiochip_close(gyMotor.BTS7960)
    gyMotor.pygame.quit()