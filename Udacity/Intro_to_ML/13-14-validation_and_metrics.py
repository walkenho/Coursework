#!/usr/bin/python

"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)

### it's all yours from here forward!  

from sklearn import tree

clf = tree.DecisionTreeClassifier()
clf.fit(features, labels)
print "Accurary of DT fitted on all data: %5.3f" %clf.score(features, labels)

from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = train_test_split(features, labels, test_size = 0.3,
        random_state = 42)

clf.fit(features_train, labels_train)
print "Accuracy of DT fitted on 0.70, tested on the remaining 0.3: %5.3f" %clf.score(features_test, labels_test)

pred = clf.predict(features_test)
number_of_predicted_pois = pred.sum()
print "Number of predicted POIs: %d." %int(number_of_predicted_pois)

print "Number of people in the test set: %d" %len(labels_test)

number_of_true_positives = sum(pred*labels_test)
print "Number of true positives: %d" %int(number_of_true_positives)

from sklearn.metrics import recall_score, precision_score
recall = recall_score(labels_test, pred)
precision = precision_score(labels_test, pred)

print "Recall: % 5.3f" %recall
print "Precision: % 5.3f" %precision
