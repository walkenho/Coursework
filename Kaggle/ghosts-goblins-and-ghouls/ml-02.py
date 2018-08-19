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
# Random Forest
################################################################################
from sklearn.ensemble import RandomForestClassifier

print() 
print("################################################################################")
print("Random Forest")
print("################################################################################")

parameters = {  'n_estimators' : [20],
                'min_samples_split' : [2, 5, 7, 10, 15, 20],
                'min_weight_fraction_leaf' : [0.0, 0.1],
                'max_leaf_nodes' : [20, 30],
                'max_depth' : [None, 5, 20, 100] }

print("Parameter Space = %s" %str(parameters))

# Extract labels:
labels_train = train["type_int"].values

for counter, predictorset in enumerate(predictors):
    features_train = train[predictorset].values

    print("\nFitting for feature set no. " + str(counter))

    rf = RandomForestClassifier(criterion = 'entropy')
    clf_rf = GridSearchCV(rf, parameters, cv=10)
    clf_rf.fit(features_train, labels_train)
    print("Best parameters: %s" %str(clf_rf.best_params_))
    print("Best score on training data: %5.3f" %clf_rf.best_score_)
    

################################################################################
# Prediction with best parameters and feature list
################################################################################

# Select best feature set:
best_feature_set = 2
best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
rf = RandomForestClassifier(criterion = "entropy", min_samples_split= 7, 
                                min_weight_fraction_leaf= 0.0, max_depth= 20, 
                                n_estimators= 20, max_leaf_nodes= 30)
rf.fit(features_train, labels_train)

test["type_int"] = rf.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_04.csv", index = False)


# Select best feature set:
best_feature_set = 1
best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:

rf = RandomForestClassifier(criterion = "entropy", min_samples_split= 2, 
                             min_weight_fraction_leaf= 0.0, max_depth= 5, 
                             n_estimators= 20, max_leaf_nodes= 20)
rf.fit(features_train, labels_train)

test["type_int"] = rf.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_05.csv", index = False)


# Select best feature set:
best_feature_set = 4
best_predictorset = predictors[best_feature_set]

features_train = train[best_predictorset].values
features_test = test[best_predictorset].values

# Fill in the details about the best classifier in the next line:
rf = RandomForestClassifier(criterion = "entropy", min_samples_split= 20, 
                             min_weight_fraction_leaf= 0.0, max_depth= 5, 
                             n_estimators= 20, max_leaf_nodes= 30)
rf.fit(features_train, labels_train)

test["type_int"] = rf.predict(features_test)
test["type"] = fprep.recast_labels(test["type_int"], "decode")

test[["id", "type"]].to_csv("submission_06.csv", index = False)
