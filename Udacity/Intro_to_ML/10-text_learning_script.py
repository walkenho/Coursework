#!/usr/bin/python

import os
import pickle
import re
import sys

sys.path.append( "../tools/" )
from parse_out_email_text import parseOutText
from sklearn.feature_extraction.text import TfidfVectorizer

from_sara  = open("from_sara.txt", "r")
from_chris = open("from_chris.txt", "r")

from_data = []
word_data = []

### temp_counter is a way to speed up the development--there are
### thousands of emails from Sara and Chris, so running over all of them
### can take a long time
### temp_counter helps you only look at the first 200 emails in the list so you
### can iterate your modifications quicker
temp_counter = 0

for name, from_person in [("sara", from_sara), ("chris", from_chris)]:
    for path in from_person:
        ### only look at first 200 emails when developing
        ### once everything is working, remove this line to run over full dataset
        
        #temp_counter += 1
        #if temp_counter < 200:
            path = os.path.join('..', path[:-1])
            print path
            email = open(path, "r")

            ### Instruction:
            ### use parseOutText to extract the text from the opened email
            ### use str.replace() to remove any instances of the words
            ### ["sara", "shackleton", "chris", "germani"]
            ### append the text to word_data
            ### append a 0 to from_data if email is from Sara, and 1 if email is from Chris
            
            stemmed_text = parseOutText(email)
            for word in ["sara", "shackleton", "chris", "germani", "sshacklensf", "sshacklmsncom", "cgermannsf"]:
                stemmed_text = stemmed_text.replace(word, "")
            
            word_data.append(stemmed_text)
            if name == "sara":
                from_data.append(0)
            else:
                from_data.append(1)
                
            email.close()
            
print "emails processed"
from_sara.close()
from_chris.close()

pickle.dump( word_data, open("your_word_data.pkl", "w") )
pickle.dump( from_data, open("your_email_authors.pkl", "w") )
