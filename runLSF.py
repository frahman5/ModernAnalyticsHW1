
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

    Run Least Squares Fitting on the relevant data
    """
    ## Seperate data into training and testing
    import csv
    import math
    import numpy

    trainingMatrix = []
    testMatrix = []

    with open(sourceDataFile) as source:
        count = 0
        reader = csv.reader(source)
        for r in reader:
            if count == 0:
                count += 1
                continue
            if count % 4 == 0:
                testMatrix.append(r)
            else:
                trainingMatrix.append(r)
            count += 1

    ## Extract training and test data
    tripTime = []
    tripDistance = []
    for row in trainingMatrix:
        tripTime.append(float(row[9]))
        tripDistance.append(float(row[10]))

    tripTimeTest = []
    tripDistanceTest = []
    for row in testMatrix:
        tripTimeTest.append(float(row[9]))
        tripDistanceTest.append(float(row[10]))

    # Run OLS on data
    x = tripDistance
    y = tripTime
    A = numpy.vstack([x, numpy.ones(len(x))]).T
    answer = numpy.linalg.lstsq(A, y)
    m, b = answer[0]
    residuals = answer[1]
    print "slope, intercept: {}, {}".format(m, b)
    print "residuals: {}".format(residuals)

    ## Calculate OLS and TLS accuracies on training data
        ## OLS accuracy 
    residuals = []
    errorsWRTAverage = [] # errors with respect to average
    average = numpy.mean(tripTimeTest) # average value in test set
    for distance, trueVal in zip(tripDistanceTest, tripTimeTest):
        predicted = (m * distance) + b # y=mx+b
        residuals.append(predicted - trueVal)
        errorsWRTAverage.append(predicted - average)
    squareResiduals = [residual * residual for residual in residuals]
    totalSquareErrors = [error * error for error in errorsWRTAverage]
    sumSquareResiduals = numpy.sum(squareResiduals)
    sumAverageError = numpy.sum(totalSquareErrors)
    print "OLS error (sum squared residuals): {}".format(sumSquareResiduals)
    print "OLS error (R^2): {}".format(1 - (sumSquareResiduals)/(sumAverageError))
        ## TLS accuracy 
    residuals = []
    for x0, y0 in zip(tripDistanceTest, tripTimeTest):
        residuals.append(orthogonalDistance(m, b, x0, y0))
    squareResiduals = [residual * residual for residual in residuals]
    print "TLS error (sum squared residuals): {}".format(numpy.sum(squareResiduals))




if __name__ == '__main__':
   #Usage: python runLFS.py sourceData.csv 
    import sys
    main(sys.argv[1])