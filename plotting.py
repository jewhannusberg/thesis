'''
Plot findings here
'''
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Seaborn color settings
col_pal = sns.color_palette("PuRd", n_colors=48)
sns.set_palette(col_pal)

LABELS = ['0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30'
, '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00'
, '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30'
, '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']


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

def plot_forecast_vs_poe(df, time, dates):
    labels = []
    for interval in df.INTERVAL_DATETIME:
        labels.append(interval)
    plt.plot(df['OPERATIONAL_DEMAND_POE10_'+time].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(df['OPERATIONAL_DEMAND_POE50_'+time].values, 'b', label='POE50', linewidth=0.75)
    plt.plot(df['OPERATIONAL_DEMAND_POE90_'+time].values, 'g', label='POE90', linewidth=0.75)
    colors = cm.rainbow(np.linspace(0, 1, len(dates)))
    # use color=colors[ix] to cycle through colour spectrum
    for ix, date in enumerate(dates):
        plt.plot(df['OPERATIONAL_DEMAND_'+date].values, color=colors[ix], linewidth=1.6)
    # plt.xticks(range(len(labels),5), labels, rotation='horizontal')
    plt.xlabel('Samples')
    plt.ylabel('Demand')
    plt.legend(loc='upper left', shadow=True)
    plt.title('Demand distributions for %s' % time)
    plt.show()

def save_all_plots(error, fname):
    '''To plot POE10 ALL vs actual'''
    plt.plot(error_POE10[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE10 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    # plt.savefig("figures/poe10/POE10_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe10/POE10_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE50 ALL vs actual'''
    plt.plot(error_POE50[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE50 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    # plt.savefig("figures/poe50/POE50_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe50/POE50_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE90 ALL vs actual'''
    plt.plot(error_POE90[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE90 forecasts for %s" % data_cleanup.remove_csv(fname))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    # plt.savefig("figures/poe90/POE90_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)
    # save to report figures also
    plt.savefig("../Report/figures/poe90/POE90_v_actual_%s.eps" % data_cleanup.remove_csv(fname), format='eps', dpi=1200)

def plot_single_day_time_error(df, date, time, poe):
    # Should take in a TIME and DATE argument to make general
    '''Plot the forecasts for that day'''
    plt.plot(df[1:-1].values, linewidth=1)
    plt.ylim([-500,1000])
    plt.xticks(range(len(df[1:-1].values)), LABELS, rotation='vertical')
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-Hour Intervals')
    plt.title('Error between %s forecast and actual for %s forecasted at %s' % (poe, date, time))
    plt.savefig("../Report/figures/%s_error/poe10_%s_daily_fcast_error.eps" % (poe.lower(), date.replace('/','')), format='eps', dpi=1200)
    # plt.show()
    # plt.close()

def plot_single_day_all_time_error(df):
    # print df[1:-1].values
    # exit()
    # f, (ax1, ax2, ax3, ax4) = plt.subplots(4, sharex=True, sharey=True)
    # ax1.plot(df[1:-1].values[0:11])
    # ax1.set_title('Sharing both axes')
    # ax2.plot(df[1:-1].values[11:22])
    # ax3.plot(df[1:-1].values[22:33])
    # ax4.plot(df[1:-1].values[33:46])

    # # Fine-tune figure; make subplots close to each other and hide x ticks for
    # # all but bottom plot.
    # # f.subplots_adjust(hspace=0)
    # plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

    plt.plot(df[1:-1].values, linewidth=0.75)
    plt.xticks(range(len(df[1:-1].values)), LABELS, rotation='vertical')

    for xc in range(1, len(df[1:-1].values-1)):
        plt.axvline(x=xc, color='k', linestyle=':', linewidth=0.25)

    plt.show()
    plt.close()