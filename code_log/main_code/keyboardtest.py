import curses
import time

# Initialize velocity values
linear_velocity = 0.0
angular_velocity = 0.0

# Constants for speed adjustments
MAX_LINEAR_VELOCITY = 2.0  # maximum forward/backward speed
MAX_ANGULAR_VELOCITY = 1.0  # maximum rotational speed
VELOCITY_INCREMENT = 0.1  # change in speed per key press

def update_velocity(key):
    global linear_velocity, angular_velocity

    # Forward and backward control
    if key == ord('w'):  # Move forward
        linear_velocity = min(linear_velocity + VELOCITY_INCREMENT, MAX_LINEAR_VELOCITY)
    elif key == ord('s'):  # Move backward
        linear_velocity = max(linear_velocity - VELOCITY_INCREMENT, -MAX_LINEAR_VELOCITY)
    else:
        linear_velocity = 0.0  # Stop if no forward/backward key is pressed

    # Left and right control
    if key == ord('a'):  # Turn left
        angular_velocity = min(angular_velocity + VELOCITY_INCREMENT, MAX_ANGULAR_VELOCITY)
    elif key == ord('d'):  # Turn right
        angular_velocity = max(angular_velocity - VELOCITY_INCREMENT, -MAX_ANGULAR_VELOCITY)
    else:
        angular_velocity = 0.0  # Stop turning if no left/right key is pressed

def main(stdscr):
    # Clear screen
    stdscr.clear()
    stdscr.nodelay(True)  # Make getch() non-blocking
    stdscr.addstr(0, 0, "Control the robot with WASD keys. Press 'q' to quit.")
    
    try:
        while True:
            key = stdscr.getch()
            
            # Exit loop if 'q' is pressed
            if key == ord('q'):
                break

            # Update velocity based on key press
            update_velocity(key)

            # Display the updated velocities
            stdscr.addstr(2, 0, f"Linear Velocity: {linear_velocity:.2f}, Angular Velocity: {angular_velocity:.2f}")
            stdscr.clrtoeol()  # Clear to end of line
            stdscr.refresh()
            time.sleep(0.1)  # Update rate (adjust as needed)

    except KeyboardInterrupt:
        pass

# Run the main function within curses wrapper
curses.wrapper(main)
