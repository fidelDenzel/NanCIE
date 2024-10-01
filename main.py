#!/usr/bin/python3

import pygame
import Actuator as nanA

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((100, 100))

def main():

    try:
        running = True
        while running:

            for event in nanA.pygame.event.get():

                if event.type == nanA.pygame.QUIT:
                    running = False
                elif event.type == nanA.pygame.KEYDOWN:

                    if event.key == nanA.pygame.K_UP:
                        nanA.move_robot('forward', nanA.current_speed)
                    
                    elif event.key == nanA.pygame.K_DOWN:
                        nanA.move_robot('backward', nanA.current_speed)
                    
                    elif event.key == nanA.pygame.K_LEFT:
                        nanA.move_robot('left', nanA.current_speed)
                    
                    elif event.key == nanA.pygame.K_RIGHT:
                        nanA.move_robot('right', nanA.current_speed)
                    
                    elif event.key == nanA.pygame.K_RETURN:
                        nanA.move_robot('spin', nanA.current_speed)    
                    
                    elif event.key >= 48 and event.key <= 57:
                        nanA.current_speed = (event.key - 48 ) * 10
                        if nanA.current_speed == 0:
                            nanA.current_speed = 100
                        print("Speed @" + str(nanA.current_speed) + " %")
                    elif event.key == nanA.pygame.K_PERIOD:
                        running = False

                elif event.type == nanA.pygame.KEYUP:
                    nanA.stop_robot()

            nanA.time.sleep(0.1)  # To avoid high CPU usage

    finally:
        print("Ending\n")
        nanA.stop_robot()
        nanA.lgpio.gpio_write(nanA.BTS7960, nanA.pin_LEN, 0)
        # nanA.lgpio.gpio_write(nanA.BTS7960, nanA.pin_REN, 0)
        nanA.lgpio.gpio_write(nanA.BTS7960, nanA.pin_LEN2, 0)
        # nanA.lgpio.gpio_write(nanA.BTS7960, nanA.pin_REN2, 0)
        nanA.lgpio.gpiochip_close(nanA.BTS7960)
        nanA.pygame.quit()

<<<<<<< HEAD
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

        # #Read Accelerometer raw value
        # Ax = gyNan.read_raw_data(gyNan.ACCEL_XOUT_H)/16384.0
        # Ay = gyNan.read_raw_data(gyNan.ACCEL_YOUT_H)/16384.0
        # Az = gyNan.read_raw_data(gyNan.ACCEL_ZOUT_H)/16384.0

        # #Read Gyroscope raw value
        # Gx = gyNan.read_raw_data(gyNan.GYRO_XOUT_H)/131.0
        # Gy = gyNan.read_raw_data(gyNan.GYRO_YOUT_H)/131.0
        # Gz = gyNan.read_raw_data(gyNan.GYRO_ZOUT_H)/131.0
        # gyNan.time.sleep(.1)

        # outpid = thetaPID.compute(stat.stdev(Gz_sample), Gz) * 1 # + thetaPID.compute(0,Ax) * 0.01 + thetaPID.compute(0,Ay) * 0.01
        
        # outpid = outpid/1.5 * 100.0
        # outpid_lim = 10.0
        # if outpid > outpid_lim:
        #     output = outpid_lim
        # elif outpid < -outpid_lim:
        #     outpid = -outpid_lim

        # print("Gz - 0 = ",Gz - stat.stdev(Gz_sample),"| output PID = ", (outpid))

        # error_th = 7.0
        # if outpid < -1 * error_th : # if negative, robot must turn ccw
        #     outpid = abs(outpid)
        #     gyMotor.move_robot('right',outpid)  #this is because output ranges from -1 to 1 due to complex numbers vector range
        # elif outpid > error_th:
        #     gyMotor.move_robot('left',10)
        # else:
        #     gyMotor.move_robot('right',0)
        #     gyMotor.move_robot('left',0)

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
=======
if __name__ == "__main__":
    main()
>>>>>>> refs/remotes/origin/master
