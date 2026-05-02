# tokenizer.py

import nltk
from nltk.stem import WordNetLemmatizer
from semantic_map import get_category

lemmatizer = WordNetLemmatizer()

def normalize(word):
    return lemmatizer.lemmatize(word.lower())

def tokenize(sentence):
    words = sentence.lower().split()
    words = [normalize(w) for w in words]
    words = [get_category(w) for w in words]
    return words