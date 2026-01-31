import numpy as np
def pid_calc(error:float,pre_error:float,time:float,kp:float,ki:float,kd:float):
  deriv = (error - pre_error) / time
  integral = error * time
  output = kp * error + ki * integral + kd * deriv
  return output