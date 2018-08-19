#!/usr/bin/python

import numpy as np
import pandas as pd
from sklearn import preprocessing

def recast_labels(series, direction):
    dict_ghost ={"Ghoul" : 1, "Goblin" : 2, "Ghost" : 3}
    inv_ghost = {v: k for k, v in dict_ghost.items()}

    if direction == "encode":
        return series.apply(lambda r: dict_ghost[r])
    elif direction == "decode":
        return series.apply(lambda r: inv_ghost[r])
    else:
        print("There was a dictionary problem")

def create_features(df):
    df["soul_hair"]  = df["has_soul"] * df["hair_length"]
    df["soul2_hair"] = df["has_soul"] * df["has_soul"] * df["hair_length"]
    df["hair_bone"]  = df["hair_length"] * df["bone_length"]
    df["soul_bone"]  = df["has_soul"] * df["bone_length"]
    df["soul_flesh"]  = df["has_soul"] * df["rotting_flesh"]
    df["bone_flesh"]  = df["bone_length"] * df["rotting_flesh"]
    df["hair_flesh"]  = df["hair_length"] * df["rotting_flesh"]

def encode_color(df):
    # When generating one-hot encoding, drop one category:
    df_color = pd.get_dummies(df["color"], drop_first = True)
    return df.join(df_color)


def get_labels_features():
    """Returns train data, test data and a list of the predictor features.
    The purpose of this function is to be able to use it together with different
    classifiers and have a standardized interface to the features in order to ease
    feature engineering. """

    ################################################################################
    # Load Data
    ################################################################################
    train = pd.read_csv("train.csv")
    test = pd.read_csv("test.csv")
    
    ################################################################################
    # Recast Labels 
    ################################################################################a
    
    train["type_int"] = recast_labels(train["type"], "encode")
    
    # Nice, but here not useful since I want to be able to encode and decode
    # in different part of the programm
    # le = preprocessing.LabelEncoder()
    # le.fit(train["type"])
    # print("Labels: " + str(le.classes_))
    # train["type_int"] = le.transform(train["type"]) 
    
    ################################################################################
    # Create Features
    ################################################################################a
    print("Generating one-hot encoding.")
    train = encode_color(train)     
    test = encode_color(test)     

    # Create features
    print("Creating features.")
    create_features(train)
    create_features(test)

    ################################################################################
    # Create predictor list
    ################################################################################

    mycolors = list(train["color"].unique())
    mycolors.sort()
    
    predictors = []
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul"] + mycolors[1:] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                  "soul_hair", "soul2_hair", "hair_bone"] + mycolors[1:] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                  "soul_hair", "hair_bone"] + mycolors[1:])
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", 
                  "soul_hair", "hair_bone"] + mycolors[1:])
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                  "soul_hair", "soul2_hair", "hair_bone", "soul_bone"] + mycolors[1:] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                  "soul_hair", "hair_bone", "soul_bone"] + mycolors[1:] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                        "soul_hair", "hair_bone", "soul_bone"] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                        "soul_hair", "hair_bone", "soul_bone", "soul_flesh", 
                        "bone_flesh", "hair_flesh"] )
    predictors.append( ["bone_length", "rotting_flesh", "hair_length", "has_soul", 
                        "soul_hair", "hair_bone", "soul_bone", "soul_flesh", 
                        "bone_flesh", "hair_flesh"] + mycolors[1:] )

    return train, test, predictors 

