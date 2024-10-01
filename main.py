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

if __name__ == "__main__":
    main()
