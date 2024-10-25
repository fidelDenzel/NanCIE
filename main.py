#!/usr/bin/python3

import time
import pygame
import Actuator as nanA
import IMU as nanImu


def main():

    try:

        # Initialize Pygame
        print("Init pygame")
        pygame.init()

        # Set up the display
        screen = pygame.display.set_mode((100, 100))
        time.sleep(1)

        # Initialize IMU
        print("Init IMU")
        nanImu.MPU_init(0x69)
        time.sleep(1)

        print("Calibrating IMU")
        roll_offset, pitch_offset = nanImu.roll_pitch_calibration(1000)
        print(f"Roll Offsets: {roll_offset}")
        print(f"Pitch Offsets: {pitch_offset}")
        time.sleep(1)

        
        #main loop
        running = True
        
        while running:
            start_time = time.time()

            # Read raw accelerometer data
            acc_x = nanImu.read_raw_data(0x3B)
            acc_y = nanImu.read_raw_data(0x3D)
            acc_z = nanImu.read_raw_data(0x3F)
            
            # Read raw gyroscope data
            gyro_x = nanImu.read_raw_data(0x43)
            gyro_y = nanImu.read_raw_data(0x45)
            gyro_z = nanImu.read_raw_data(0x47)
            
            # Convert gyroscope data to degrees per second
            gyro_x = gyro_x / 131.0
            gyro_y = gyro_y / 131.0
            gyro_z = gyro_z / 131.0
            
            # Calculate accelerometer angles
            accel_roll, accel_pitch = nanImu.get_accel_angle(acc_x, acc_y, acc_z)
            dt = 0.08
            roll_th = nanImu.complementary_filter(gyro_value=gyro_x,accel_value=accel_roll,dt=dt)
            pitch_th = nanImu.complementary_filter(gyro_value=gyro_y,accel_value=accel_pitch,dt=dt)

            print(f"Roll: {(roll_th - roll_offset):.2f}°, Pitch: {(pitch_th - pitch_offset):.2f}°")
            
            # for event in pygame.event.get():

            #     if event.type == pygame.QUIT:
            #         running = False
            #     elif event.type == pygame.KEYDOWN:

            #         if event.key == pygame.K_UP:
            #             nanA.move_robot('forward', nanA.current_speed)
                    
            #         elif event.key == pygame.K_DOWN:
            #             nanA.move_robot('backward', nanA.current_speed)
                    
            #         elif event.key == pygame.K_LEFT:
            #             nanA.move_robot('left', nanA.current_speed)
                    
            #         elif event.key == pygame.K_RIGHT:
            #             nanA.move_robot('right', nanA.current_speed)
                    
            #         elif event.key == pygame.K_RETURN:
            #             nanA.move_robot('spin', nanA.current_speed)    
                    
            #         elif event.key >= 48 and event.key <= 57:
            #             nanA.current_speed = (event.key - 48 ) * 10
            #             if nanA.current_speed == 0:
            #                 nanA.current_speed = 100
            #             print("Speed @" + str(nanA.current_speed) + " %")
            #         elif event.key == pygame.K_PERIOD:
            #             running = False

            #     elif event.type == pygame.KEYUP:
            #         nanA.stop_robot()
                # time.sleep(0.001)  # To avoid high CPU usage
            
            # elapsed_time = time.time() - start_time
            # time_to_sleep = dt - elapsed_time
            # print(time_to_sleep)
            time.sleep(0.1)
            
            # if time_to_sleep > 0:
            #     time.sleep(time_to_sleep)

    finally:
        nanA.end_robot()
        pygame.quit()

if __name__ == "__main__":
    main()
