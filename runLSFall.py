
def orthogonalDistance(slope, intercept, x0, y0):
    """
    Calculate the orthogonal distance from a line with slope and intercept
    to the point (x0, yo)
    """
    import math
    numerator = math.fabs((slope * x0) - y0 + intercept)
    denominator = math.sqrt((slope * slope) + 1)

    return float(numerator)/float(denominator)

def main(sourceDataFile, m, b):
    """
    string float float -> None

    Report OLS and TLS accuracy of the linear model y = mx + b 
    on data in sourceDataFile
    """
    ## Extract test data
    import csv
    import math
    import numpy

    # trainingMatrix = []
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

    ## Extract training and test data
    print "extracting triptime and tripdistance arrays"
    # tripTime = []
    # tripDistance = []
    # for row in trainingMatrix:
    #     tripTime.append(float(row[9]))
    #     tripDistance.append(float(row[10]))

    tripTimeTest = []
    tripDistanceTest = []
    count = 0
    for row in testMatrix:
        if count % 500000 == 0:
             print "count: {}".format(count)
        tripTimeTest.append(float(row[9]))
        tripDistanceTest.append(float(row[10]))
        count +=1

    # # Run OLS on data
    # x = tripDistance
    # y = tripTime
    # A = numpy.vstack([x, numpy.ones(len(x))]).T
    # answer = numpy.linalg.lstsq(A, y)
    # m, b = answer[0]
    # residuals = answer[1]
    # print "slope, intercept: {}, {}".format(m, b)
    # print "residuals: {}".format(residuals)

    ## Calculate OLS and TLS accuracies on test data
        ## OLS accuracy 
    print "calculating accuracy"
    residuals = []
    errorsWRTAverage = [] # errors with respect to average
    average = numpy.mean(tripTimeTest) # average value in test set
    yBar = average
    xBar = numpy.mean(tripDistanceTest)
    xMinusXBar = []
    yMinusYBar = []
    count = 0
    for distance, trueVal in zip(tripDistanceTest, tripTimeTest):
        if count % 500000 == 0:
            print "count (calcing residuals) {}".format(count)
        predicted = (m * distance) + b # y=mx+b
        residuals.append(predicted - trueVal)
        count += 1
        errorsWRTAverage.append(predicted - average)
        xMinusXBar.append(distance - xBar)
        yMinusYBar.append(trueVal - yBar)
    print "calculating square residuals"
    squareResiduals = [residual * residual for residual in residuals]
    print "calculating square errors"
    totalSquareErrors = [error * error for error in errorsWRTAverage]
    print "summing errors and reproting results"
    sumSquareResiduals = numpy.mean(squareResiduals)
    sumAverageError = numpy.mean(totalSquareErrors)
    print "calculating correlation coefficient"
    corNumerator = numpy.sum([(xDif * yDif) for xDif, yDif in zip(xMinusXBar, yMinusYBar)])
    xSTD = math.sqrt(numpy.sum([xDif * xDif for xDif in xMinusXBar]))
    ySTD = math.sqrt(numpy.sum([yDif * yDif for yDif in yMinusYBar]))
    r = corNumerator / (xSTD * ySTD)
    print "OLS error (sum squared residuals): {}".format(sumSquareResiduals)
    # print "OLS error (R^2): {}".format(1 - (sumSquareResiduals)/(sumAverageError))
    print "Correlation Coefficient: {}".format(r)
        ## TLS accuracy 
    residuals = []
    for x0, y0 in zip(tripDistanceTest, tripTimeTest):
        residuals.append(orthogonalDistance(m, b, x0, y0))
    squareResiduals = [residual * residual for residual in residuals]
    print "TLS error (sum squared residuals): {}".format(numpy.mean(squareResiduals))




if __name__ == '__main__':
   #Usage: python runLFS.py sourceData.csv m b
    import sys
    main(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]))
