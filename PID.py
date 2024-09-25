class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0
        self.integral = 0

    def compute(self, setpoint, current_value):
        """
        Compute the PID control output based on the setpoint (target value) and current_value.
        """
        # Calculate error
        error = setpoint - current_value
        
        # Proportional term
        P_out = self.Kp * error
        
        # Integral term
        self.integral += error
        I_out = self.Ki * self.integral
        
        # Derivative term
        derivative = error - self.previous_error
        D_out = self.Kd * derivative
        
        # Total output
        output = P_out + I_out + D_out
        
        # Store error for next derivative calculation
        self.previous_error = error
        
        return output

    def reset(self):
        """
        Reset the integral and previous error for PID control.
        """
        self.previous_error = 0
        self.integral = 0