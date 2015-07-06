def convertTimeToPlottable(timeString):
    """
    string -> float
    e.g '11:23:14' -> 11.38
    """
    hour, minute, second  = timeString.split(':')
    return float(hour) + float(float(minute)+ float(second)/60)/60.0

def orthogonalDistance(slope, intercept, x0, y0):
    """
    Calculate the orthogonal distance from a line with slope and intercept
    to the point (x0, yo)
    """
    import math
    numerator = math.fabs((slope * x0) - y0 + intercept)
    denominator = math.sqrt((slope * slope) + 1)

    return float(numerator)/float(denominator)

def main(sourceDataFile):
    """
    string -> None

    Train a linear regression using OLS on the data in sourceDataFile
    """
    ## Extract test data
    import csv
    import math
    import numpy

    trainingMatrix = []
    print "opening csv into python object"
    with open(sourceDataFile) as source:
        count = 0
        reader = csv.reader(source)
        for r in reader:
            if count == 0:
                print "Header: {}".format(r)
                count += 1
                continue
            #if count == 1000:
               # print "TAKE OUT EARLY BREAK BEFORE GETTING FINAL RESULT"
               # break
            trainingMatrix.append(r)
            count += 1

    ## Create the feature vecotrs
    tripTime = []
    tripDistance = []
    straightTripDistance = []
    plat = []
    plong = []
    dlat = []
    dlong = []
    pickupTimeRawest = []
    count = 0 
    for row in trainingMatrix:
        if len(row) == 14:
            continue
        if count % 500000 == 0:
             print "count (training Matrix read): {}".format(count)
        tripTime.append(float(row[9]))
        tripDistance.append(float(row[10]))
        straightTripDistance.append(float(row[15]))
        plat.append(float(row[12]))
        plong.append(float(row[11]))
        dlat.append(float(row[14]))
        dlong.append(float(row[13]))
        pickupTimeRawest.append(row[6])
        count +=1
    ## Transform pickupTime to a binary variable
    pickupTime = []
    #from calcGraphs import convertTimeToPlottable
    #import pdb
    #pdb.set_trace()
    pickupTimeRaw = [convertTimeToPlottable(time.split()[1]) for time in pickupTimeRawest]
    for time in pickupTimeRaw:
        if (5 <= time) and (time <= 17):
            pickupTime.append(1)
        else:
            assert (time < 5) or (time > 17)
            pickupTime.append(0)

    ## Normalize each feature (turn it into a standard gaussian with mean 0, std 1)
    print "normalizing features"
    for featureList in (tripDistance, straightTripDistance, plat, plong, dlat, dlong, pickupTime):
        mean = numpy.mean(featureList)
        std = numpy.std(featureList)
        for index, elem in enumerate(featureList):
            featureList[index] = (float(elem) - mean)/float(std) 
   
    ## Run multiple linear regression (OLS) on data
    import pandas as pd
    import statsmodels.api as sm
 
    listOfFeatures = (tripDistance, straightTripDistance, plat, plong, dlat, dlong, pickupTime)
    namesOfFeatures = ['TripDistance', 'StraightTripDistance', 'PLat', 'PLong', 'DLat', 'DLong', 'PickupTime']
    dfColumnDict = {index:pd.Series(thing[0], name=thing[1]) for index, thing in enumerate(zip(listOfFeatures, namesOfFeatures))}
    X = pd.DataFrame({
        'TripDistance':pd.Series(tripDistance, name='TripDistance'),
        'StraightTripDistance':pd.Series(straightTripDistance, name='StraightTripDistance'),
        'PLat':pd.Series(plat, name='PLat'), 
        'PLong':pd.Series(plong, name='PLong'), 
        'DLat':pd.Series(dlat, name='DLat'), 
        'DLong':pd.Series(dlong, name='Dlong'), 
        'PickupTime':pd.Series(pickupTime, name='PickupTime')}) 
#X = pd.concat(dfColumnDict.values(), axis=1)
    #import pdb
    #pdb.set_trace()
#X = pd.DataFrame(listOfFeatures, columns=['TripDistance', 'StraightTripDistance', 'PLat', 'PLong', 'DLat', 'DLong', 'PickupTime'])
    y = pd.Series(tripTime, name='TripTime')
    
    X = sm.add_constant(X)
    #import pdb
    #pdb.set_trace()
    fit = sm.OLS(y, X).fit()
    print fit.summary() 

if __name__ == '__main__':
   #Usage: python runLFS.py sourceData.csv
    import sys
    main(sys.argv[1])
