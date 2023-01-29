import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MaxAbsScaler
import warnings

warnings.filterwarnings("ignore")#Used to ignore 10 fold cross validation user warning

#knn(X, y, metric, trainingPer): Computes and returns accuracy of k nearest neighbour classifier model as well as the optimal k value to use for the model
#Takes in data with X and labels for the data y, a distance metric to be used in the form of 1(manhattan) or 2(Euclidian) and a percentage of data to use for training the model(ex. 0.10 for 10%)
#knn splits the inputted X and y data into training and testing sets according to trainingPer inputted
#knn then finds the optimal k value to use for the given training data using GridSearchCV
#knn then generates a Model Using the K nearest neighbour Classifier using the optimal k value
#knn finally computes the accuracy of the modle then returns it along with the k value used
def knn(X, y, metric, trainingPer):
    #Splitting data into inpputted amount
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=trainingPer)

    #Computing Optimal k value for training data using gridCV
    tempKnn = KNeighborsClassifier(p=metric)
    param_grid = {'n_neighbors': [1,3,5,7]}
    tempKnnGridSearch = GridSearchCV(tempKnn, param_grid, cv=5)
    tempKnnGridSearch.fit(X_train, y_train)
    optimalK = list(tempKnnGridSearch.best_params_.values())[0]

    #Creating KNN model with optimal k, predicting test set using model, then returning accuracy score
    knn = KNeighborsClassifier(n_neighbors=optimalK, p=metric)
    knn.fit(X_train, y_train)
    pred = knn.predict(X_test)

    return accuracy_score(y_test, pred)*100, optimalK

#repeatKnn(X, y, metric, trainingPer): Uses inputted values to compute a knn model 10 times then returns the mean accuracy, standard deviation and most common k value used from all models computed
#Takes in same data as knn func above and passes it into the knn function 10 times
#Records accuracy and k value used for each model then stores them in accuracies and kVals respectibly
#Finally repeatKnn returns the mean value of the accuracies list, standard deviation value of accuracies list and thhe most common k value inside kVals
#NOTE: For more accurate results, knn models should be computed 100 times but for the sake of our programs run time, I chose to only computer knn 10 times but the table provided in the project report was computed by running knn 100 times
def repeatKnn(X, y, metric, trainingPer):
    accuracies = []#Stores accuracy of each knn model computed
    kVals = []#Stores k value used in each knn model
    for i in range(0,3):#Loop runs knn model 10 times and stores accuracies and kvalues used
        tempAcc, tempK = knn(X, y, metric, trainingPer)
        accuracies.append(tempAcc)
        kVals.append(tempK)

    return np.mean(accuracies), np.std(accuracies), max(set(kVals), key=kVals.count)


#SOURCE FOR DEC_SCALE
#https://stackoverflow.com/questions/52971959/decimal-point-normalization-in-python
#Dec_scale(df): takes in a data set and performs decimal normalization on it then returns normalizaed data
def Dec_scale(df):
    for x in df:
        p = df[x].max()
        q = len(str(abs(p)))
        df[x] = df[x]/10**q
    return df

#Reading in parkinsons data and storing data in X with target values/labels in y
file_name = "parkinsons.csv"
df = pd.read_csv(file_name)
df = df.drop('name', axis=1)#removing name attribute as its unnecesary
X = df.drop('status', axis=1)
y = df['status']

#GENERATING ALL NORMALIZED DATA SETS AND STORING IN allData[]
allData = []#Holds original raw data as well as all normalized data sets
allData.append(X)
#Generating min max scaled values
minMaxScaler = MinMaxScaler()
minMaxScaledX = minMaxScaler.fit_transform(X)
allData.append(minMaxScaledX)
#Generating z score scaled values
zScoreScaler = StandardScaler()
zScoreScaledX = zScoreScaler.fit_transform(X)
allData.append(zScoreScaledX)
#Generating max scaled values
absMaxScaler = MaxAbsScaler()
absMaxScaledX = absMaxScaler.fit_transform(X)
allData.append(absMaxScaledX)
#Generating decimal scaled values
decimalScaledX = Dec_scale(X)
allData.append(decimalScaledX)


#MAIN LOOP USED TO CALCULATE VALUES AND FILL IN TABLE
file = open('results.txt', 'w')
file.write("Training(%)\tMetric\t\t\tRaw Data\t\tMin-Max\t\t\tZ-Score\t\t\tMax\t\t\tDecimal\n")
trainingPer = 0.05
for i in range(0, 19):#Loop for each training %
    file.write("{}\t\t".format(round(trainingPer * 100, 1)))
    for j in range(1,3):#Loop for each metric(Euclidian and Manhattan)
        if(j == 1):#Printing Euclidian distance metric line
            rawD, rawSTD, rawDK = repeatKnn(allData[0], y, 2, trainingPer)#computing models accuracy and k value used for for raw data with manhattan metric and inputted training set %
            minMaxD, minMaxSTD, minMaxDK = repeatKnn(allData[1], y, 2, trainingPer)
            zScoreD, zScoreSTD, zScoreDK = repeatKnn(allData[2], y, 2, trainingPer)
            maxD, maxSTD, maxDK = repeatKnn(allData[3], y, 2, trainingPer)
            decimalD, decimalSTD, decimalDK = repeatKnn(allData[4], y, 2, trainingPer)
            file.write("Euclidian\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\n".format(rawD, rawSTD, rawDK, minMaxD, minMaxSTD, minMaxDK, zScoreD, zScoreSTD, zScoreDK, maxD, maxSTD, maxDK, decimalD, decimalSTD, decimalDK))
        if (j == 2):#Printing Manhattan distance metric line
            rawD, rawSTD, rawDK = repeatKnn(allData[0], y, 1, trainingPer)#computing models accuracy and k value used for for raw data with manhattan metric and inputted training set %
            minMaxD, minMaxSTD, minMaxDK = repeatKnn(allData[1], y, 1, trainingPer)
            zScoreD, zScoreSTD, zScoreDK = repeatKnn(allData[2], y, 1, trainingPer)
            maxD, maxSTD, maxDK = repeatKnn(allData[3], y, 1, trainingPer)
            decimalD, decimalSTD, decimalDK = repeatKnn(allData[4], y, 1, trainingPer)
            file.write("\t\tManhattan\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\t\t{:0.2f}+-{:0.2f}({})\n".format(rawD, rawSTD, rawDK, minMaxD, minMaxSTD, minMaxDK, zScoreD, zScoreSTD, zScoreDK, maxD, maxSTD, maxDK, decimalD, decimalSTD, decimalDK))
    trainingPer += 0.05

