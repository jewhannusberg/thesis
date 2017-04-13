'''
Plot findings here
'''
import numpy as np
import matplotlib.pyplot as plt

def plot_error(error, actual_demand):
    x_ax =  np.arange(len(error.OPERATIONAL_DEMAND))
    fig, ax = plt.subplots(1)
    ax.plot(error.OPERATIONAL_DEMAND_POE10, label='POE10 error')
    ax.plot(error.OPERATIONAL_DEMAND_POE50, label='POE50 error')
    ax.plot(error.OPERATIONAL_DEMAND_POE90, label='POE90 error')
    ax.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)
    ax.legend(loc='upper_left', shadow=True)
    ax.set_ylim(-1500, 1500)
    # ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE10)
    # ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE50)
    # ax.fill_between(x_ax, 0, error.OPERATIONAL_DEMAND_POE90)

    # Include time taken from filename
    ax.set_title('Error variation')
    plt.show()

def plot_exceedance(forecasted_demand, actual_demand, count_POE, dist=10):
    plt.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)
    # change the following line to only deal with a sinle day's worth of data
    plt.plot(forecasted_demand['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(count_POE, label='POE'+str(dist), linewidth=1.5)
    plt.title('POE'+str(dist)+' Exceedance of Actual Demand')
    plt.legend(loc='upper_left', shadow=False)
    plt.show()

def plot_data(demand_poe, actual_demand):
    # plot projected demand @ all POE
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE50'].values, 'b', label='POE50', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE90'].values, 'g', label='POE90', linewidth=0.75)
    # Overlay actual demand
    plt.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)
    plt.legend(loc='upper left', shadow=True)
    plt.title('Demand distributions for %s' % forecast_names[0])
    plt.show()
