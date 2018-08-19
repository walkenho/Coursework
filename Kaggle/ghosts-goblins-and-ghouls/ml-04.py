#!/usr/bin/python

import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
import numpy as np
import pandas as pd
import feature_preparation as fprep

################################################################################
# Running feature preparation script
################################################################################

# imports features and data
train, test, predictors = fprep.get_labels_features()

print("Performing ML on %d feature set(s)." %len(predictors))

################################################################################
# Discriminant Analysis
################################################################################
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

print() 
print("################################################################################")
print("Linear Discriminant Analysis")
print("################################################################################")

parameters = {'shrinkage':['auto',None]}

print("Parameter Space = %s" %str(parameters))

# Extract labels:
labels_train = train["type_int"].values

for counter, predictorset in enumerate(predictors):
    features_train = train[predictorset].values

    print("\nFitting for feature set no. " + str(counter))

    clf = LinearDiscriminantAnalysis(solver = "eigen")

    clf_grid = GridSearchCV(clf, parameters)
    clf_grid.fit(features_train, labels_train)

    print("Best parameters: %s" %str(clf_grid.best_params_))
    print("Best score on training data: %7.5f" %clf_grid.best_score_)
 
print() 
print("################################################################################")
print("Quadratic Discriminant Analysis")
print("################################################################################")

parameters = {'reg_param':[0.0, 0.1, 0.15, 0.16, 0.17, 0.18, 0.2, 0.25, 0.3, 0.4,  0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 1.0]}

print("Parameter Space = %s" %str(parameters))

# Extract labels:
labels_train = train["type_int"].values

for counter, predictorset in enumerate(predictors):
    features_train = train[predictorset].values

    print("\nFitting for feature set no. " + str(counter))

    clf = QuadraticDiscriminantAnalysis()

    clf_grid = GridSearchCV(clf, parameters)
    clf_grid.fit(features_train, labels_train)

    print("Best parameters: %s" %str(clf_grid.best_params_))
    print("Best score on training data: %7.5f" %clf_grid.best_score_)
    

   

################################################################################
# Prediction with best parameters and feature list
################################################################################
#
## Select best feature set:
best_feature_set = 6
best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
clf = QuadraticDiscriminantAnalysis(reg_param=0.15)
clf.fit(features_train, labels_train)

test["type_int"] = clf.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_08.csv", index = False)

