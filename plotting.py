'''
Plot findings here
'''
import numpy as np
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from data_cleanup import remove_csv
from data_cleanup import convert_date

# Seaborn color settings
col_pal = sns.color_palette("RdGy", n_colors=48)
sns.set_palette(col_pal)

LABELS = ['0:30', '1:00', '1:30', '2:00', '2:30', '3:00', '3:30', '4:00', '4:30', '5:00', '5:30'
, '6:00', '6:30', '7:00', '7:30', '8:00', '8:30', '9:00', '9:30', '10:00', '10:30', '11:00', '11:30', '12:00'
, '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', '17:00', '17:30', '18:00', '18:30'
, '19:00', '19:30', '20:00', '20:30', '21:00', '21:30', '22:00', '22:30', '23:00', '23:30']


def plot_error(error, actual_demand):
    plt.clf()
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
    plt.close()
    plt.clf()

def plot_exceedance(forecasted_demand, actual_demand, count_POE, dist=10):
    plt.clf()
    plt.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)
    # change the following line to only deal with a sinle day's worth of data
    plt.plot(forecasted_demand['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(count_POE, label='POE'+str(dist), linewidth=1.5)
    plt.title('POE'+str(dist)+' Exceedance of Actual Demand')
    plt.legend(loc='upper_left', shadow=False)
    plt.show()
    plt.close()
    plt.clf()

def plot_data(demand_poe, actual_demand):
    # plot projected demand @ all POE
    plt.clf()
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE10'].values, 'r', label='POE10', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE50'].values, 'b', label='POE50', linewidth=0.75)
    plt.plot(demand_poe['OPERATIONAL_DEMAND_POE90'].values, 'g', label='POE90', linewidth=0.75)
    # Overlay actual demand
    plt.plot(actual_demand['OPERATIONAL_DEMAND'].values, 'k:', label='Actual Demand', linewidth=1.5)
    plt.legend(loc='upper left', shadow=True)
    plt.title('Demand distributions for %s' % forecast_names[0])
    plt.show()
    plt.close()
    plt.clf()

def plot_forecast_vs_poe(df, time, dates):
    plt.clf()
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
    plt.clf()

def save_all_plots(error_POE10, error_POE50, error_POE90, actual_demand, fname, prefix, date):
    plt.clf()
    '''To plot POE10 ALL vs actual'''
    plt.plot(error_POE10[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE10 forecasts for %s%s" % (prefix, date))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("../Report/figures/poe10/all_data/POE10_v_actual_%s.eps" % remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE50 ALL vs actual'''
    plt.plot(error_POE50[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE50 forecasts for %s%s" % (prefix, date))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("../Report/figures/poe50/all_data/POE50_v_actual_%s.eps" % remove_csv(fname), format='eps', dpi=1200)

    '''To plot POE90 ALL vs actual'''
    plt.plot(error_POE90[1:-1].values, linewidth=0.25)
    plt.plot(actual_demand.values, color='k', linewidth=2)
    plt.title("Actual demand against all POE90 forecasts for %s%s" % (prefix, date))
    plt.xlabel('Samples')
    plt.ylabel('Demand (MW)')
    plt.savefig("../Report/figures/poe90/all_data/POE90_v_actual_%s.eps" % remove_csv(fname), format='eps', dpi=1200)
    plt.clf()

def plot_single_day_time_error(df, date, time, poe, prefix):
    # Should take in a TIME and DATE argument to make general
    '''Plot the forecasts for that day'''
    plt.clf()
    plt.plot(df[1:-1].values, linewidth=1)
    plt.ylim([-500,1000])
    plt.xticks(range(len(df[1:-1].values)), LABELS, rotation='vertical')
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-Hour Intervals')
    plt.title('Error between %s forecast and actual for %s forecasted at %s' % (poe, date, time))
    plt.savefig("../Report/figures/%s/single_day_forecast/%s%s_daily_fcast_error.eps" % (poe.lower(), prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.clf()


def plot_poex_single_time_error(data_series, poe50_series, poe90_series, time, prefix, date):
    plt.clf()
    col_pal = sns.color_palette("cubehelix", n_colors=3)
    sns.set_palette(col_pal)
    plt.plot(data_series[1:-1].values, label='POE10 error at 0000', linewidth=0.75)
    plt.plot(poe50_series[1:-1].values, label='POE50 error at 0000', linewidth=0.75)
    plt.plot(poe90_series[1:-1].values, label='POE90 error at 0000', linewidth=0.75)
    plt.xticks(range(len(data_series[1:-1].values)), LABELS, rotation='vertical')
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-hour Interval')
    plt.title('All level POE error for initial forecasts %s%s' % (prefix, date))
    plt.legend(loc='upper left', shadow=True)
    plt.savefig("../Report/figures/single_daytime_error_all/%s%s_fcast_error_poex.eps" % (prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.clf()

def plot_poex_single_time_full_error(poe10_all, poe50_all, poe90_all, time, prefix, date):
    plt.clf()
    col_pal = sns.color_palette("husl", n_colors=3)
    sns.set_palette(col_pal)
    plt.plot(poe10_all[1:-1].values, label='Full POE10 error at 0000', linewidth=0.75)
    plt.plot(poe50_all[1:-1].values, label='Full POE50 error at 0000', linewidth=0.75)
    plt.plot(poe90_all[1:-1].values, label='Full POE90 error at 0000', linewidth=0.75)
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-hour Interval')
    plt.title('All level POE error for initial forecasts beginning from %s%s extended' % (prefix, date))
    plt.legend(loc='upper left', shadow=True)
    plt.savefig("../Report/figures/single_time_error_all/%s%s_all_stime_error_poex.eps" % (prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.clf()

def plot_single_day_all_time_error(df, date, poe, prefix):
    plt.clf()
    # Seaborn color settings
    col_pal = sns.color_palette("RdGy", n_colors=48)
    sns.set_palette(col_pal)
    plt.plot(df[1:-1].values, linewidth=0.75)
    # plt.xticks(range(len(df[1:-1].values)), LABELS, rotation='vertical')

    for xc in range(1, len(df[1:-1].values-1)):
        plt.axvline(x=xc, color='k', linestyle=':', linewidth=0.25)

    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-Hour Intervals')
    plt.title('Error between %s forecast and actual for %s forecasted at all times' % (poe, date))
    # plt.savefig("../Report/figures/%s/single_day_all_forecast/%s%s_fcast_error.eps" % (poe.lower(), prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.show()
    plt.close()
    plt.clf()

def plot_med_avg_error(avg_vals, med_vals, poe, date, prefix):
    plt.clf()
    col_pal = sns.color_palette("cubehelix", n_colors=3)
    sns.set_palette(col_pal)
    plt.plot(avg_vals[1:-1].values, color="#ff4d4d", label='Average Error', linewidth=0.75)
    plt.plot(med_vals[1:-1].values, color="#6699ff", label='Median Error', linewidth=0.75)
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-Hour Intervals')
    plt.title('%s: Average error against median error for %s%s' % (poe, prefix, date))
    # plt.xticks(range(len(avg_vals[1:-1].values)), LABELS, rotation='vertical')    
    # for xc in range(1, len(avg_vals[1:-1].values-1)):
        # plt.axvline(x=xc, color='k', linestyle=':', linewidth=0.25)
    plt.legend(loc='upper left', shadow=True)
    plt.savefig("../Report/figures/%s/avg_med/%s%s_avg_med_error.eps" % (poe.lower(), prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.clf()

def plot_all_errors_one_graph(fname, POE10_data, POE50_data, POE90_data, date, prefix):
    plt.clf()
    col_pal = sns.color_palette("cubehelix", n_colors=3)
    sns.set_palette(col_pal)
    plt.plot(POE10_data.values[1], label='POE10 Error', linewidth=0.75)
    plt.plot(POE50_data.values[1], label='POE50 Error', linewidth=0.75)
    plt.plot(POE90_data.values[1], label='POE90 Error', linewidth=0.75)
    plt.title('POE10, POE50, and POE90 average errors for %s%s' % (prefix, date))
    plt.legend(loc='upper left', shadow=True)
    plt.ylabel('Demand Error (MW)')
    plt.xlabel('Half-Hour Intervals')
    plt.savefig("../Report/figures/error_all/avg_error_poex_%s%s.eps" % (prefix, date.replace('/','')), format='eps', dpi=1200)
    plt.clf()

def plot_exceedance_num(x_ax, prefix, date):
    plt.clf()
    col_pal = sns.color_palette("cubehelix", n_colors=3)
    sns.set_palette(col_pal)
    x_labels = ['POE10', 'POE50', 'POE90']
    plt.xticks(range(len(x_ax)), x_labels, rotation='vertical')
    bar_chart = plt.bar(range(len(x_labels)), x_ax)
    bar_chart[0].set_color(sns.xkcd_rgb["light blue grey"])
    bar_chart[1].set_color(sns.xkcd_rgb["seaweed green"])
    bar_chart[2].set_color(sns.xkcd_rgb["light periwinkle"])
    for a,b in zip(range(len(x_ax)), x_ax):
        plt.text(a, b, str(b))
    plt.ylabel('Frequency of Forecast Exceeding Actual')
    plt.xlabel('POE Level')
    plt.title('Frequency of each POE level exceeding actual demand for %s%s' % (prefix, date))
    plt.savefig("../Report/figures/poe_exceed/exceeds_act_freq_%s%s.eps" % (prefix, date.replace('/','')), format='eps', dpi=1200)
    # plt.show()
    # plt.close()
    plt.clf()