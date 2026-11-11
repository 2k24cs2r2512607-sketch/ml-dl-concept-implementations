
import streamlit as st
import pickle
import string
import nltk
import os

from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# Download required NLTK resources
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

# Text preprocessing
def transform_text(text):
    text = text.lower()
    tokens = word_tokenize(text)

    y = []

    for i in tokens:
        if i.isalnum():
            y.append(i)

    y = [
        i for i in y
        if i not in stop_words and i not in string.punctuation
    ]

    y = [ps.stem(i) for i in y]

    return " ".join(y)


# Load model and vectorizer relative to app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'vectorizer.pkl'), 'rb') as f:
    tfidf = pickle.load(f)

with open(os.path.join(BASE_DIR, 'model.pkl'), 'rb') as f:
    model = pickle.load(f)


# Streamlit interface
st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter your message")

if st.button('Predict'):

    if not input_sms.strip():
        st.warning("Kindly enter a message first.")

    else:
        transformed_sms = transform_text(input_sms)

        vector_input = tfidf.transform([transformed_sms])

        result = model.predict(vector_input)[0]

        if result == 1:
            st.error("Spam Message!")
        else:
            st.success("Not Spam (Ham)!")
