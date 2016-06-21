from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

def trapezoidal_rule_simplified(base_sum, height):
    return (height)*(base_sum)/2

def plot_matplotlib_fig(datetime_vector, current_vector, initial_index, final_index):

    datetime_range = datetime_vector[initial_index:final_index]
    current_range  = current_vector[initial_index:final_index]

    #INTEGRAL
    #finding trapezoid heights
    heights = [(y-x).total_seconds() for x,y in zip(datetime_range[1:], datetime_range[:-1])]

    #finding the sum of trapezoid bases
    bases_sum = [(y+x) for x,y in zip(current_range[1:],  current_range[:-1])]

    #Calculating the approximated area under the curve
    trapz = [trapezoidal_rule_simplified(x,y) for x,y in zip(bases_sum,heights)]
    ampere_hour = sum(trapz)/3600 #calculated in seconds

    #TODO: Comment debug
    #print("List of trapezoid heights: ", heights)
    #print("List of trapezoid bases_sum: ", bases_sum)
    #print("List of trapezoidal areas: ", trapz)
    #print("Area under the curve (Ampere/Seconds):", sum(trapz))
    #print("Final return: Ampere/Hour = ", ampere_hour)


    #PLOT
    #create the canvas and plot the series
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot(datetime_vector, current_vector, marker = 'o' )
    ax.fill_between(datetime_range,0, current_range, facecolor='blue', alpha=0.5)

    #set plot limits
    ax.set_xlim([min(datetime_vector), max(datetime_vector)])
    ax.set_ylim([min(current_vector)*0.9, max(current_vector)*1.1])

    #format the ticks
    #xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S') #with year-month-date
    xfmt = mdates.DateFormatter('%H:%M:%S') #only time, no dates
    ax.xaxis.set_major_formatter(xfmt)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.set_ylabel('Current (mA)',fontsize=14)
    ax.grid(True)

    # rotates and right aligns the x labels, and moves the bottom of the
    # axes up to make room for them
    fig.autofmt_xdate()
    fig.suptitle('Battery Current (last {0} points)'.format(len(current_vector)), fontsize=16)
    plt.savefig('BatteryCurrent')

    #TODO: Comment this line
    #plt.show()
    return ampere_hour

