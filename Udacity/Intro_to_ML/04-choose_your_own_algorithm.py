#!/usr/bin/python

import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
import numpy as np

features_train, labels_train, features_test, labels_test = makeTerrainData()


### the training data (features_train, labels_train) have both "fast" and "slow"
### points mixed together--separate them so we can give them different colors
### in the scatterplot and identify them visually
grade_fast = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==0]
bumpy_fast = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==0]
grade_slow = [features_train[ii][0] for ii in range(0, len(features_train)) if labels_train[ii]==1]
bumpy_slow = [features_train[ii][1] for ii in range(0, len(features_train)) if labels_train[ii]==1]


visualization = False
#### initial visualization
if visualization == True:
    plt.xlim(0.0, 1.0)
    plt.ylim(0.0, 1.0)
    plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
    plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
    plt.legend()
    plt.xlabel("bumpiness")
    plt.ylabel("grade")
    plt.show()
################################################################################


### your code here!  name your classifier object clf if you want the 
### visualization code (prettyPicture) to show you the decision boundary


################################################################################
# Decision Tree
################################################################################
from sklearn import tree

print "################################################################################"
print "DT"
print "################################################################################"
print 
print "Optimizing a DT by hand:"
min_sample_list = [2, 5, 10, 15, 20, 25, 30, 35, 40, 50, 100]
score_list = []
for min_samples in min_sample_list:
    #print 
    #print "Decision Tree - min_samples_split = %d" %min_samples
    clf2 = tree.DecisionTreeClassifier(min_samples_split = min_samples)
    clf2.fit(features_train, labels_train)
    scores = cross_validation.cross_val_score(clf2, features_train, labels_train)
    print "For min_samples = %d, the score on training (cross-val) and test data are %5.3f and %5.3f" \
    %(min_samples, scores.mean(), clf2.score(features_test, labels_test))
    score_list.append(scores.mean())
print 
print "Best score on training data: %5.3f" %((max(score_list)))

# But it is a lot more convenient doing this automatized.
# A good tool for this is GridSearchCV.
# GridSearch Uses 3-fold Crossvalidation as standard

print
print "And optimizing it using GridSearchCV:"
parameters = {'min_samples_split' : min_sample_list}
dsr = tree.DecisionTreeClassifier()
clf_tree = GridSearchCV(dsr, parameters)
clf_tree.fit(features_train, labels_train)
print "Best parameters: %s" %str(clf_tree.best_params_)
print "Best score on training data: %5.3f" %clf_tree.best_score_
print "Score on test data: %5.3f" %clf_tree.score(features_test, labels_test)


#try:
#    prettyPicture(clf, features_test, labels_test)
#except NameError:
#    pass

################################################################################
# SVM
################################################################################
from sklearn import svm

print 
print "################################################################################"
print "SVC"
print "################################################################################"

parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10, 100, 1000, 5000, 10000, 15000]}
print "Parameter Space = %s" %str(parameters)

svr = svm.SVC()
clf_svc = GridSearchCV(svr, parameters)
clf_svc.fit(features_train, labels_train)
print "Best parameters: %s" %str(clf_svc.best_params_)
print "Best score on training data: %5.3f" %clf_svc.best_score_
print "Score on test data: %5.3f" %clf_svc.score(features_test, labels_test)

print "Fitting with all training data."
clf = svm.SVC(kernel = 'rbf', C = 10000)
clf.fit(features_train, labels_train)
print clf.score(features_test, labels_test)

#try:
#    prettyPicture(clf, features_test, labels_test)
#except NameError:
#    pass


################################################################################
# Random Forest
################################################################################
from sklearn.ensemble import RandomForestClassifier

print 
print "################################################################################"
print "Random Forest"
print "################################################################################"

parameters = {'n_estimators':[10, 100], 'min_samples_split' : min_sample_list}
print "Parameter Space = %s" %str(parameters)

rf = RandomForestClassifier()
clf_rf = GridSearchCV(rf, parameters)
clf_rf.fit(features_train, labels_train)
print "Best parameters: %s" %str(clf_rf.best_params_)
print "Best score on training data: %5.3f" %clf_rf.best_score_
print "Score on test data: %5.3f" %clf_rf.score(features_test, labels_test)


################################################################################
# AdaBoost
################################################################################
from sklearn.ensemble import AdaBoostClassifier

print 
print "################################################################################"
print "AdaBoost"
print "################################################################################"

parameters = {'base_estimator': [tree.DecisionTreeClassifier()]}
print "Parameter Space = %s" %str(parameters)

ada = AdaBoostClassifier()
clf_ada = GridSearchCV(ada, parameters)
clf_ada.fit(features_train, labels_train)
print "Best parameters: %s" %str(clf_ada.best_params_)
print "Best score on training data: %5.3f" %clf_ada.best_score_
print "Score on training data: %5.3f" %clf_ada.score(features_train, labels_train)
print "Score on test data: %5.3f" %clf_ada.score(features_test, labels_test)

