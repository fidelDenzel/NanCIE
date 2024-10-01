#!/usr/bin/python3

import pygame
import Actuator as nanA
import IMU as nanImu
import time


def main():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((100, 100))

    # Initialize IMU
    nanImu.MPU_init()
    dt = 0.01

    try:
        #calibrate sensor => offsets
        # accel_offsets, gyro_offsets = nanImu.calibrate_mpu6050(num_samples=2000)
        
        #main loop
        running = True
        while running:
            start_time = time.time()

            # # Read raw accelerometer data
            # acc_x = nanImu.read_raw_data(0x3B) - accel_offsets['x']
            # acc_y = nanImu.read_raw_data(0x3D) - accel_offsets['y']
            # acc_z = nanImu.read_raw_data(0x3F) - accel_offsets['z']
            
            # # Read raw gyroscope data
            # gyro_x = nanImu.read_raw_data(0x43) - gyro_offsets['x']
            # gyro_y = nanImu.read_raw_data(0x45) - gyro_offsets['y']
            # gyro_z = nanImu.read_raw_data(0x47) - gyro_offsets['z']
            
            # # Convert gyroscope data to degrees per second
            # gyro_x = gyro_x / 131.0
            # gyro_y = gyro_y / 131.0
            # gyro_z = gyro_z / 131.0
            
            # # Calculate accelerometer angles
            # accel_roll, accel_pitch = nanImu.get_accel_angle(acc_x, acc_y, acc_z)

            # roll_th = nanImu.complementary_filter(gyro_value=gyro_x,accel_value=accel_roll,dt=dt)
            # pitch_th = nanImu.complementary_filter(gyro_value=gyro_y,accel_value=accel_pitch,dt=dt)
            # print(f"Roll: {roll_th:.2f}°, Pitch: {pitch_th:.2f}°")
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_UP:
                        nanA.move_robot('forward', nanA.current_speed)
                    
                    elif event.key == pygame.K_DOWN:
                        nanA.move_robot('backward', nanA.current_speed)
                    
                    elif event.key == pygame.K_LEFT:
                        nanA.move_robot('left', nanA.current_speed)
                    
                    elif event.key == pygame.K_RIGHT:
                        nanA.move_robot('right', nanA.current_speed)
                    
                    elif event.key == pygame.K_RETURN:
                        nanA.move_robot('spin', nanA.current_speed)    
                    
                    elif event.key >= 48 and event.key <= 57:
                        nanA.current_speed = (event.key - 48 ) * 10
                        if nanA.current_speed == 0:
                            nanA.current_speed = 100
                        print("Speed @" + str(nanA.current_speed) + " %")
                    elif event.key == pygame.K_PERIOD:
                        running = False

                elif event.type == pygame.KEYUP:
                    nanA.stop_robot()
                time.sleep(0.001)  # To avoid high CPU usage
            
            elapsed_time = time.time() - start_time
            time_to_sleep = dt - elapsed_time
            
            # if time_to_sleep > 0:
            #     time.sleep(time_to_sleep)

    finally:
        nanA.end_robot()
        pygame.quit()

if __name__ == "__main__":
    main()
