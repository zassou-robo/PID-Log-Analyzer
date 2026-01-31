import numpy as np
def pid_calc(error,pre_error,time,kp,ki,kd):
  deriv = (error - pre_error) / time
  integral = error * time
  output = kp * error + ki * integral + kd * deriv
  return output