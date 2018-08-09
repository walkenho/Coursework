#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess

### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()

#########################################################

from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

#########################################################
print "GaussianNB (which is the one that they want on the course)"
clf_GaussianNB = GaussianNB()
t0 = time()
clf_GaussianNB.fit(features_train, labels_train)
t1 = time()
print "Training time:", round(t1-t0, 3), "s"
print "Accuracy on training data = " + str(clf_GaussianNB.score(features_train, labels_train))

t2 = time()
pred_GaussianNB = clf_GaussianNB.predict(features_test)
t3 = time()

print "Testing time = ", round(t3-t2, 3), "s"
print "Accuracy on test data = " + str(accuracy_score(pred_GaussianNB, labels_test))

#########################################################
print "MultinomialNB"
clf_multinomialNB = MultinomialNB()
clf_multinomialNB.fit(features_train, labels_train)
print "Accuracy on training data = " + str(clf_multinomialNB.score(features_train, labels_train))
print "Accuracy on test data = " + str(clf_multinomialNB.score(features_test, labels_test))

#########################################################
print "BernoulliNB"
clf_BernoulliNB= BernoulliNB()
clf_BernoulliNB.fit(features_train, labels_train)
print "Accuracy on training data = " + str(clf_BernoulliNB.score(features_train, labels_train))
print "Accuracy on test data = " + str(clf_BernoulliNB.score(features_test, labels_test))


