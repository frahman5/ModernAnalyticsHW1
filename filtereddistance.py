#!usr/local/bin/python

## Takes in a csv of taxicab data and outputs a filtered dataset of 
## ride distances. Filters by removing all data outside of 3 standard deviations
## from the mean

def filterData(distances, originalDatasetFile, newDatasetName):
    """
    list string string -> None

    Creates a csv ("newDatasetName.csv") of filtered data, where we throw
    out all data that has a trip Distance greater than 3 std outside the mean6
    """
    import numpy
    import pandas

    ## Open the original dataset into a dataframe
    df = pandas.read_csv(originalDatasetFile)

    ## Add a new distance column to it
    distancesSeries = pandas.Series(distances)
    df['TripDistance'] = distancesSeries

    ## Remove columns with "error" in distance column
    df = df[df.TripDistance != 'ERROR']

    ## Remove columns with trip distance outside 3 sigma of mean
    mean = numpy.mean(df.TripDistance)
    std = numpy.std(df.TripDistance)
    numSigma = 3
    df = df[df.TripDistance < (mean + numSigma*std)]
    df = df[df.TripDistance > (mean - numSigma*std)]
    df = df[df.TripDistance < 250] # Get rid of annoying monstrous outlier

    ## Write the dataframe to a file
    df.to_csv('{}.csv'.format(newDatasetName))

    print "Mean: {}".format(mean)
    print "Std: {}".format(std)
    print "Threw out {} ".format(len(distances) - len(df)) + \
          "pieces of data from dataset (> {}std away)".format(numSigma)

if __name__ == '__main__':
    # Usage: python filtereddistance.py 'data.csv' nameOfOutputDataFile
    import sys
    import pandas as pd
    from distance import get_distance
    from pprint import pprint

    distances = []
    error_count  = 0
    
    # create a pandas dataframe with the location data
    df = pd.read_csv(sys.argv[1])
    dfWithLocData = df[['pickup_longitude','pickup_latitude','dropoff_longitude', 'dropoff_latitude']]

    for index, plong, plat, dlong, dlat in dfWithLocData.itertuples():
        plong = float(plong)
        plat = float(plat)
        dlong = float(dlong)
        dlat = float(dlat)
        try:
            distances.append(get_distance(plat,plong,dlat,dlong))
        except:
            distances.append('ERROR')
            error_count += 1
            print plat, plong, dlat, dlong
            print error_count

    filterData(distances, sys.argv[1], sys.argv[2])


