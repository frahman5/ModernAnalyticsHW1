#! usr/bin/python

# Create graphs of 
    # 1) trip distance vs. trip time (s)
    # 2) pick up time vs. trip time(s)
    # 3) distance btwn pickup and dropoff vs. trip time(s)

def convertTimeToPlottable(timeString):
    """
    string -> float
    e.g '11:23' -> 11.38
    """
    hour, minute = timeString.split(':')
    return float(hour) + float(minute)/60.0

def calcGraphs(filteredDataFile):
    """
    string -> None

    """
    import math
    import pandas as pd
    import matplotlib.pyplot as plt
    

    ## Get the data into arrays
    df = pd.read_csv(filteredDataFile)
        ## trip distance
    tripDistance = list(df['trip_distance'])
        ## pickup time
    pickupTimeFullString = list(df['pickup_datetime'])
    pickupTimeGoodString = [time.split()[1] for time in pickupTimeFullString]
    pickupTime = [convertTimeToPlottable(time) for time in pickupTimeGoodString]
    # pickupTimeBinary = []
    # for time in pickupTime:
    #     if time <= 12:
    #         pickupTimeBinary.append(0)
    #     else:
    #         pickupTimeBinary.append(1)
    pickupTimeMinutesFromTheHour = []
    for time in pickupTime:
        pickupTimeMinutesFromTheHour.append((time - int(time)) * 60)
        ## distance btwn pickup and dropoff
    dBPD = list(df['TripDistance'])
        ## trip time in seconds
    tripTime = list(df['trip_time_in_secs'])

    ## Plot the data
    yAxis = tripTime
    for xAxis, xLabel, plotNum in   [(pickupTimeMinutesFromTheHour, 'Pickup Time (Minutes from last hour)', 0),
                                    (pickupTimeMinutesFromTheHour, 'Pickup Time (Minutes from last hour)', 0)]:
    # ((tripDistance, 'Trip Distance (miles)', 1), 
                                    # (pickupTime, 'Pickup Time (hours since midnight)', 2),
                                    # (dBPD, 'Straight Line Trip Distance (miles)', 3)):
        # Basic plot configurations
        fig = plt.figure()
        plot = fig.add_subplot(
                    111 # 111 is 1x1 grid, 1st subplot (1x1 = 1 row, 1 column)
                    )
        plot.scatter(xAxis, yAxis)

        # Plot labels and titles
        plot.set_xlabel(xLabel)
        plot.set_ylabel('Trip Time (s)')
        plot.set_title('Trip Time (s) vs {}'.format(xLabel))

        # Save the plot
        plt.savefig("plotMinutesFromHour{}".format(plotNum))

# [(pickupTimeBinary, 'Pickup Time Binary (hours since midnight)', 0),
                                    # (pickupTimeBinary, 'Pickup Time Binary (hours since midnight)', 0)]:

if __name__ == '__main__':
    # Usage: python calcGraphs.py filteredData.csv
    import sys

    calcGraphs(sys.argv[1])
