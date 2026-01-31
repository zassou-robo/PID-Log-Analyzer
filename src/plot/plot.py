import matplotlib.pyplot as plt
import numpy as np

def plot_all(t, goal, actual):
    goal = np.array(goal)
    actual = np.array(actual)
    err = goal - actual
    e = abs(err)
    fig, ax = plt.subplots()
    ax.plot(t, goal, label='goal')
    ax.plot(t, actual, label='actual')
    ax.scatter(t, err, c='blue', label='error')
    ax.legend()
    plt.show()
