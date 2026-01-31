from src.calc.pid_calc import pid_calc
from src.plot.plot import plot_all

goal,actual,time,error,pre_error = 10.5,0,0.01,0,0
time_history = []
goal_history = []
actual_history = []

for i in range(100): 
  error = goal - actual
  output = pid_calc(error,pre_error,time,0.2,0.1,0.0)
  print(actual)
  actual += output
  time_history.append(i * time)
  goal_history.append(goal)
  actual_history.append(actual)
  pre_error = error

plot_all(time_history, goal_history, actual_history)