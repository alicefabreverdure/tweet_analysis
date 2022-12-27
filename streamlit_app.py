import datetime as dt
import re

import pandas as pd
import streamlit as st
from flair.data import Sentence
from flair.models import TextClassifier
import base64

import tweepy as tp
from tweepy import OAuthHandler

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

### TWEET SEARCH AND CLASSIFY ###
st.subheader('Search Twitter for Query')

query = st.text_input('Query:', '#')
# Choose number of tweets
option = st.selectbox(
    'How many tweets ?',
    (10, 50, 100))

if query != '' and query != '#':
    with st.spinner(f'Searching for and analyzing {query}...'):
        # initialisation
        consumer_key = "neFjQUU9CfE9gFgBK2X4yro2j" # API/Consumer key
        consumer_secret = "orhQzemgSx07sMV9lTK197j7ZTXrojnDwdGMQdDA1RUl2Gli5h" # API/Consumer Secret Key
        access_token = "1204779047252889609-0dCHKl8ZNqCLLmJCBuqP1rULpXYLLY"    # Access token key
        access_token_secret = "kiY8AIFf4MBOBQGxTbNf3DRCmYYklZT0e87m5SClYvnnX" # Access token Secret key

        # Authentification
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tp.API(auth)
        # Get English tweets from the past 4 weeks
        no_of_tweets = option # change to unlimited

        #The number of tweets we want to retrieved from the search
        tweets = api.search_tweets(q=query, count=no_of_tweets)

        def twitter_scrap():
            attributes_container = [[tweet.id, tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source,  tweet.text
                        , tweet.lang] for tweet in tweets]

            # On def les colonnes du dataframe
            columns = ["ID","User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet", "Lang"]
            #On créé un Df:
            tweets_df = pd.DataFrame(attributes_container, columns=columns)
            tweets_df["Address"]= query
            return tweets_df

        tweets_df = twitter_scrap()     

        pos_vs_neg = {'__label__0': 0, '__label__4': 0}

        # Add data for each tweet
        for tweet in tweets:
            # Skip iteration if tweet is empty
            if tweet.text in ('', ' '):
                continue
            # Make predictions
            sentence = Sentence(preprocess(tweet.text))
            classifier.predict(sentence)
            sentiment = sentence.labels[0]
            # Keep track of positive vs. negative tweets
            pos_vs_neg[sentiment.value] += 1
            # Append new data
            tweets_df = tweets_df.append({'tweet': tweet.text, 'predicted-sentiment': sentiment}, ignore_index=True)
try:
    st.write(tweets_df)
    try:
        st.write('Percentage positive tweet:', pos_vs_neg['__label__4'], '%')
        st.write('Percentage negative tweet:', pos_vs_neg['__label__0'],'%')
    except ZeroDivisionError: # if no negative tweets
        st.write('All postive tweets')
except NameError: # if no queries have been made yet
    pass

st.caption('Authors : Hugo Favre, Loris Bulliard, Michel Daher Mansour, Alice Fabre-Verdure')