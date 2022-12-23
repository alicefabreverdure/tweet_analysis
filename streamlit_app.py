import datetime as dt
import re

import pandas as pd
import streamlit as st
from flair.data import Sentence
from flair.models import TextClassifier
import base64

#page_bg_img = '''
#<style>
#p {
#ackground-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
#ackground-size: cover;
#
#/style>
#''

#st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown( """
   <style>
   [data-testid="stAppViewContainer"] {
   background-image: url("https://images.unsplash.com/photo-1551817958-20204d6ab212?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OXx8dHdlZXR8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60");
   -webkit-background-size: cover;
   -moz-background-size: cover;
   -o-background-size: cover;
   background-size: cover;
   }

   [data-testid="stHeader"] {
    background: rgba(0,0,0,0);
    }

   </style>   """,   unsafe_allow_html=True
   )

   # Set page title
st.title('Twitter Sentiment Analysis')

# Load classification model
with st.spinner('Loading classification model...'):
    classifier = TextClassifier.load('model-saves/best-model.pt')

import re

allowed_chars = ' AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789~`!@#$%^&*()-=_+[]{}|;:",./<>?'
punct = '!?,.@#'
maxlen = 280

def preprocess(text):
    return ''.join([' ' + char + ' ' if char in punct else char for char in [char for char in re.sub(r'http\S+', 'http', text, flags=re.MULTILINE) if char in allowed_chars]])[:maxlen]

st.subheader('Single tweet classification')

tweet_input = st.text_input('Tweet:')

if tweet_input != '':
    # Pre-process tweet
    sentence = Sentence(preprocess(tweet_input))

    # Make predictions
    with st.spinner('Predicting...'):
        classifier.predict(sentence)

    # Show predictions
    label_dict = {'__label__0': 'Negative', '__label__4': 'Positive'}

    if len(sentence.labels) > 0:
        st.write('Prediction:')
        st.write(label_dict[sentence.labels[0].value] + ' with ',
                sentence.labels[0].score*100, '% confidence')

st.caption('Authors : Hugo Favre, Loris Bulliard, Michel Daher Mansour, Alice Fabre-Verdure')

