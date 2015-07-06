
def orthogonalDistance(W, point):
    """
    tuple tuple -> float

    Calculate the distance from the given point to the line y=WX
    """
    assert len(W) == 8
    assert len(point) == 8
    import numpy as np
    import math

    ## parametrize the line (y = A + tN where A is a point on the line, t 
    ## a scalar and N a unit vector in the direction of the line)
    normW = math.sqrt(np.dot(W, W))
    A = (0,0,0,0,0,0,0, W[7])
    N = [float(item)/normW for item in W]

    ## Calculate the distance using d = || (A-point) - ((A-point)*N)N||
    AMinPoint = [a_i - p_i for a_i, p_i in zip(A, point)]
    AMinPointDotN = np.dot(AMinPoint, N)
    AMinPointDotNTimesN = [AMinPointDotN * ni for ni in N]
    dVector = [LHS - RHS for LHS, RHS in zip(AMinPoint, AMinPointDotNTimesN)]
    d = math.sqrt(np.dot(dVector, dVector))
    
    return d

def main(sourceDataFile, w):
    """
    string tuple -> None

    Report OLS accuracy, TLS accuracy and correlation coefficient for linear model w
    on data in sourceDataFile
    """
    ## Extract test data
    import csv
    import math
    import numpy as np

    testMatrix = []
    print "opening csv into python object"
    with open(sourceDataFile) as source:
        count = 0
        reader = csv.reader(source)
        for r in reader:
            if count == 0:
                count += 1
                continue
            testMatrix.append(r)
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

    for row in testMatrix:
        if len(row) == 14:
            continue
        if count % 500000 == 0:
             print "count (test Matrix read): {}".format(count)
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
    from runLSFTrain import convertTimeToPlottable
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
        mean = np.mean(featureList)
        std = np.std(featureList)
        for index, elem in enumerate(featureList):
            featureList[index] = (float(elem) - mean)/float(std)
   
    featureMatrix = [dlat, dlong, plat, plong, pickupTime, straightTripDistance, tripDistance, [1 for elem in dlat]]
    ## Calculate OLS, TLS, and correlation between expected and predicted values
    olsResiduals = []
    tlsResiduals = []
    predictedVals = []
    for index in range(len(dlat)):
        X = [featureMatrix[column][index] for column in range(8)]
        predicted = np.dot(w, X)
        trueVal = tripTime[index]
        point = list(X)
        point[-1] = trueVal
        olsResiduals.append(predicted - trueVal)
        tlsResiduals.append(orthogonalDistance(w, point))
        predictedVals.append(predicted)
    squareOLSResiduals = [residual * residual for residual in olsResiduals]
    squareTLSResiduals = [residual * residual for residual in tlsResiduals]
    OLSError = np.mean(squareOLSResiduals)
    TLSError = np.mean(squareTLSResiduals)
    r = np.corrcoef(predictedVals, tripTime)[0][1]

    print "OLS accuracy: {}".format(OLSError)
    print "TLS accuracy: {}".format(TLSError)
    print "Correlation between predicted and expected values: {}".format(r)
    
   

if __name__ == '__main__':
   #Usage: python runLFSTest.py sourceData.csv w
   #e.g: python runLSFTest.py trip_data_1.csv "1, 2, 3, 4, 5, 6, 7, 8"
    import sys
    W = [float(elem) for elem in sys.argv[2].split(',')]
    print "Running with W: {}".format(W)
    main(sys.argv[1], W)
