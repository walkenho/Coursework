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
# Neural Network
################################################################################

from sklearn import neural_network

import warnings
warnings.filterwarnings("ignore")

print() 
print("################################################################################")
print("Neural Network")
print("################################################################################")

parameters = {  'activation':['logistic','relu'], 
                'hidden_layer_sizes':[10,15,25], 
                'alpha':[1e-4, 1e-3, 1e-2, 1e-1], 
                'solver':['lbfgs','sgd'], 
                'learning_rate':['constant', 'adaptive']}

print("Parameter Space = %s" %str(parameters))

# Extract labels:
labels_train = train["type_int"].values

for counter, predictorset in enumerate(predictors):
    features_train = train[predictorset].values

    print("\nFitting for feature set no. " + str(counter))

    nnet = neural_network.MLPClassifier()

    clf_nnet = GridSearchCV(nnet, parameters, cv = StratifiedKFold(3))
    clf_nnet.fit(features_train, labels_train)

    print("Best parameters: %s" %str(clf_rf.best_params_))
    print("Best score on training data: %7.5f" %clf_rf.best_score_)
    

################################################################################
# Prediction with best parameters and feature list
################################################################################

# Select best feature set:
best_feature_set = 0
best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
nnet = neural_network.MLPClassifier()
nnet.fit(features_train, labels_train)

test["type_int"] = nnet.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_07.csv", index = False)

