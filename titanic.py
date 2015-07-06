## A python script to run logistic regression
## on the kaggle titanic disaster challenge
## takes test.csv and train.csv to determine if a passegner survived
## depending on gender, age and passenger class

import pandas as pd                     # dataframes
import numpy as np
import statsmodels.api as sm 

def intifySex(string):
    if string == 'male':
        return 1
    elif string == 'female':
        return 0
    else:
        raise ValueError('sex is {}'.format(string))

def intifyProbability(p):
    assert (p >= 0) and (p <= 1)
    if p < 0.5:
        return 0
    else:
        return 1
def main(trainFile, testFile):
    # Read the data into a pandas dataframe
    df = pd.read_csv(trainFile)
    ## Create dummy variables for passengar class, to keep coefficients comparable
    ## Since a class of "4" isn't actually 4 times more mathematically meaningful
    ## than a clas of "1", we make dummy variables to prevent issues
    dummyNames = {1:'FirstClass', 2: 'SecondClass', 3: 'ThirdClass'}
    for Pclass in df['Pclass'].unique():
        df[dummyNames[int(Pclass)]] = (df['Pclass'] == Pclass)

    ## Create a training dataframe
    df = df[df['Age'].notnull()]            ## Filter out data with no age variable
    trainDF = df[['Survived', 'Sex', 'Age', 'FirstClass', 'SecondClass', 'ThirdClass']]
    trainDF['Sex'] = trainDF['Sex'].apply(intifySex)
    trainDF['FirstClass'] = trainDF['FirstClass'].apply(lambda c: int(c))
    trainDF['SecondClass'] = trainDF['SecondClass'].apply(lambda c: int(c))
    trainDF['ThirdClass'] = trainDF['ThirdClass'].apply(lambda c: int(c))
    trainCols = trainDF[['Sex', 'Age', 'FirstClass', 'SecondClass', 'ThirdClass']]
    trainCols['intercept'] = 1.0
    predictedCol = trainDF['Survived']

    # Run the logistic regression
    logit = sm.Logit(predictedCol, trainCols)
    result = logit.fit()
    print result.summary()

    # # Create a test dataframe
    testDF = pd.read_csv(testFile)
    outputDF = testDF     # for outputting results
    median = np.median(testDF['Age'])   
    #print median                       
    testDF['Age'].replace('Nan', median, inplace = True)           
    for Pclass in testDF['Pclass'].unique():
        testDF[dummyNames[int(Pclass)]] = (testDF['Pclass'] == Pclass)
    testDF = testDF[['Sex', 'Age', 'FirstClass', 'SecondClass', 'ThirdClass']]
    testDF['Sex'] = testDF['Sex'].apply(intifySex)
    testDF['FirstClass'] = testDF['FirstClass'].apply(lambda c: int(c))
    testDF['SecondClass'] = testDF['SecondClass'].apply(lambda c: int(c))
    testDF['ThirdClass'] = testDF['ThirdClass'].apply(lambda c: int(c))
    X = testDF[['Sex', 'Age', 'FirstClass', 'SecondClass', 'ThirdClass']]
    X['intercept'] = 1.0
   

    # for index, sex, age, firstClass, secondClass, thirdClass, intercept in X.itertuples():
    #     y = logit.predict([sex, age, firstClass, secondClass, thirdClass, intercept])
    #     print y   
    # Create predictions on test data
    survivalChanceProb = []
    for index, sex, age, firstclass, secondclass, thirdclass in testDF.itertuples():
        survivalChanceProb.append(result.predict([sex, age, firstclass, secondclass, thirdclass, 1.0]))
        #print result.predict([sex, age, firstclass, secondclass, thirdclass, 1.0])

    #write probabilties and pass id's to a data file
    survivalChance = [intifyProbability(prob) for prob in survivalChanceProb]
    df = pd.concat([outputDF['PassengerId'], pd.Series(survivalChance, name = "Survived")], axis = 1)
    df.to_csv('{}.csv'.format('Titanic_predictions'), index = False)




if __name__ == '__main__':
    import sys

    main(sys.argv[1], sys.argv[2])