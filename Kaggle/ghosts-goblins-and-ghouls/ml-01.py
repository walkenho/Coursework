#!/usr/bin/python

import matplotlib.pyplot as plt
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
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
# SVC
################################################################################
from sklearn import svm

print()
print("################################################################################")
print("SVC")
print("################################################################################")

parameters = {'kernel':('linear', 'rbf'), 'C':[0.1, 1, 10, 100, 1000, 10000, 15000]}
print("Parameter Space = %s" %str(parameters))

# Extract labels:
labels_train = train["type_int"].values

for counter, predictorset in enumerate(predictors):
    features_train = train[predictorset].values

    print("\nFitting for feature set no. " + str(counter))
    
    svr = svm.SVC()
    clf_svc = GridSearchCV(svr, parameters, cv=10)
    clf_svc.fit(features_train, labels_train)
    print("Best parameters: %s" %str(clf_svc.best_params_))
    print("Best score on training data: %5.3f" %clf_svc.best_score_)


################################################################################
# Prediction with best parameters and feature list
################################################################################

# Select best feature set:
best_feature_set = 6

best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
svc = svm.SVC(kernel = "linear", C = 10)
svc.fit(features_train, labels_train)

test["type_int"] = svc.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_03.csv", index = False)

#########################################################################
# Another submission
#########################################################################

# Select best feature set:
best_feature_set = 7

best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
svc = svm.SVC(kernel = "linear", C = 10)
svc.fit(features_train, labels_train)

test["type_int"] = svc.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_09.csv", index = False)

