import PID
import GyrometerMPU6050 as gyNan
import MotorInterface as gyMotor
import statistics as stat
import time

thetaPID = PID.PIDController(1,0,0)
linePID = PID.PIDController(0,0,0)
mpu = gyNan.MPU_init(0x69)

Gz_sample = []

try:

    for i in range(0,10):
        #Read Accelerometer raw value
        Ax = gyNan.read_raw_data(gyNan.ACCEL_XOUT_H)/16384.0
        Ay = gyNan.read_raw_data(gyNan.ACCEL_YOUT_H)/16384.0
        Az = gyNan.read_raw_data(gyNan.ACCEL_ZOUT_H)/16384.0

        #Read Gyroscope raw value
        Gx = gyNan.read_raw_data(gyNan.GYRO_XOUT_H)/131.0
        Gy = gyNan.read_raw_data(gyNan.GYRO_YOUT_H)/131.0
        Gz = gyNan.read_raw_data(gyNan.GYRO_ZOUT_H)/131.0

        gyNan.time.sleep(.1)

        Gz_sample.append(Gz)

    print(stat.mean(Gz_sample), "\n", Gz_sample, "\n", stat.stdev(Gz_sample))

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
        gyNan.time.sleep(.1)

        outpid = thetaPID.compute(stat.stdev(Gz_sample), Gz) * 0.98 + thetaPID.compute(0,Ax) * 0.01 + thetaPID.compute(0,Ay) * 0.01
        print("Gz - 0 = ",Gz - stat.stdev(Gz_sample),"output PID = ", int(outpid))

        for event in gyMotor.pygame.event.get():

            if event.type == gyMotor.pygame.QUIT:
                running = False
            elif event.type == gyMotor.pygame.KEYDOWN:
                
                # if event.key == gyMotor.pygame.K_b:
                #     outpid = thetaPID.compute(stat.stdev(Gz_sample), Gz) * 0.98 + ...
                #     thetaPID.compute(0,Ax) * 0.01 + ...
                #     thetaPID.compute(0,Ay) * 0.01
                #     print("Gz - 0 = ",Gz - stat.stdev(Gz_sample),"output PID = ", int(outpid))
                    # if outp < 0 : # if negative, robot must turn ccw
                    #     gyMotor.move_robot('right',100)  #this is because output ranges from -1 to 1 due to complex numbers vector range
                    # elif outp > 0 :
                    #     gyMotor.move_robot('left',100)

                if event.key == gyMotor.pygame.K_UP:
                    gyMotor.move_robot('forward', gyMotor.current_speed)
                
                elif event.key == gyMotor.pygame.K_DOWN:
                    gyMotor.move_robot('backward', gyMotor.current_speed)
                
                elif event.key == gyMotor.pygame.K_LEFT:
                    gyMotor.move_robot('left', gyMotor.current_speed)
                
                elif event.key == gyMotor.pygame.K_RIGHT:
                    gyMotor.move_robot('right', gyMotor.current_speed)
                
                elif event.key == gyMotor.pygame.K_RETURN:
                    gyMotor.move_robot('spin', gyMotor.current_speed)    
                
                elif event.key >= 48 and event.key <= 57:
                    gyMotor.current_speed = (event.key - 48 ) * 10
                    if gyMotor.current_speed == 0:
                        gyMotor.current_speed = 100
                    print("Speed @" + str(gyMotor.current_speed) + " %")

            elif event.type == gyMotor.pygame.KEYUP:
                gyMotor.stop_robot()

        gyMotor.time.sleep(0.1)  # To avoid high CPU usage

finally:
    print("Ending\n")
    gyMotor.stop_robot()
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_LEN, 0)
    # gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_REN, 0)
    gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_LEN2, 0)
    # gyMotor.lgpio.gpio_write(gyMotor.BTS7960, gyMotor.pin_REN2, 0)
    gyMotor.lgpio.gpiochip_close(gyMotor.BTS7960)
    gyMotor.pygame.quit()