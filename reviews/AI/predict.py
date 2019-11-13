import string 
import joblib
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

def predict(test):
    filename = 'C:\\Users\\liu_w\\Documents\\unBiased\\reviews\\AI\\model.joblib'
    loaded_model = joblib.load(filename)
    result = loaded_model.predict([test])
    return result