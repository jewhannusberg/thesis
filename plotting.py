'''
Plot findings here
'''
import numpy as np
import matplotlib.pyplot as plt
def plot_error(error):
    x_ax =  np.arange(len(error.OPERATIONAL_DEMAND))
    fig, ax = plt.subplots(1)
    ax.plot(error.OPERATIONAL_DEMAND_POE10, label='POE10 error')
    ax.plot(error.OPERATIONAL_DEMAND_POE50, label='POE50 error')
    ax.plot(error.OPERATIONAL_DEMAND_POE90, label='POE90 error')
    ax.legend(loc='upper_left', shadow=True)
    ax.set_ylim(-500, 500)
    ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE10)
    ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE50)
    ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE90)
    ax.set_title('Error variation')
    plt.show()