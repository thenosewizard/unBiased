
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
import json  
import numpy as np
import pandas as pd  
from pandas.io.json import json_normalize 
import numpy as np
import string 
#from build import customStepsPipline, tokenizer
import joblib
#!pip install spacy
#!python -m spacy download en
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

import string 
#!pip install spacy
#!python -m spacy download en
import spacy
from spacy.lang.en.stop_words import STOP_WORDS












#creating a list for punctuations
punc = string.punctuation
#list of stop_words
nlp = spacy.load('en')
from spacy.lang.en import English
stopWords = spacy.lang.en.stop_words.STOP_WORDS
engToken = English()


#add more steps later
class customStepsPipline(TransformerMixin):
    def transform(self, X, **transform_params):
        #clean the text
        return [clean_text(text) for text in X]
        
    #no parameters that it needs to know
    def fit(self, X, y=None, **fit_params):
        return self
    
    def get_params(self, deep=True):
        return {}

    
# Basic function to clean the text
def clean_text(text):
    # Removing spaces and converting text into lowercase
    return text.strip().lower()  


def tokenizer(review):
    tokens = engToken(review)
    
    #lemmitation
    #Assigning the base forms of words. For example, 
    #the lemma of “was” is “be”, and the lemma of “rats” is “rat”.
    lemmi_tokens =[]
    for word in tokens:
        if word.lemma_ != "-PRON-":
            lemmi_tokens.append(word.lemma_.lower().strip())
        else:
            lemmi_tokens.append(word.lower_)        
    #removing the stop words
    #stop words such as a, the, is, we, they
    stop_words = [word for word in lemmi_tokens if not word in stopWords and word not in punc]
            
    #return the processed list of tokens
    return stop_words


def run():
    df_steam = pd.read_csv("C:\\Users\\abich\OneDrive\\School Stuff\\P2\Assignment 1\\fsd-p2\\reviews\\AI\\large.csv")
    df_steam["weighted_vote_score"].astype(float)
    df_steam["weighted_vote_score"] = df_steam["weighted_vote_score"].round(decimals=3)



    df_plot = df_steam[['review', 'weighted_vote_score']].dropna()
    df_steam["bad"] = df_steam["weighted_vote_score"].apply(lambda x: 1 if x > 0.546 else 0)


    punc = string.punctuation
    nlp = spacy.load('en')
    from spacy.lang.en import English
    stopWords = spacy.lang.en.stop_words.STOP_WORDS
    engToken = English()

    bow_vector = CountVectorizer(tokenizer = tokenizer,lowercase = True, ngram_range=(1,1)) 
    tfidf_vector = TfidfVectorizer(tokenizer = tokenizer)



    from sklearn.model_selection import train_test_split
    X = df_steam['review'] #input
    ylabels = df_steam['bad'] #output
    X_train, X_test, y_train, y_test = train_test_split(X, ylabels, test_size= 0.3)

    # Logistic Regression Classifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.metrics import accuracy_score
    classifier =  LogisticRegression()
    #!pip install joblib
    #LogisticRegression()
    # Create pipeline using Bag of Words
    pipe = Pipeline([("cleaner", customStepsPipline()),
                ('vectorizer', bow_vector),
                ('classifier', classifier)])


    from sklearn import metrics
    pipe.fit(X_train,y_train)
    predicted = pipe.predict(X_test)

    # Model Accuracy
    print("Accuracy:",metrics.accuracy_score(y_test, predicted))
    print("Precision:",metrics.precision_score(y_test, predicted))
    print("Recall:",metrics.recall_score(y_test, predicted))
    joblib.dump(pipe, 'scaled_tree_clf.pkl') 

def predicter(test):
    filename = 'C:\\Users\\abich\OneDrive\\School Stuff\\P2\Assignment 1\\fsd-p2\\reviews\\AI\\scaled_tree_clf.pkl'
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([test])
    return result