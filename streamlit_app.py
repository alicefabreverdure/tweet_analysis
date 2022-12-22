import datetime as dt
import re

import pandas as pd
import streamlit as st
from flair.data import Sentence
from flair.models import TextClassifier
from twitterscraper import query_tweets
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