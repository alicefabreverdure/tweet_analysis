import pytest # importing our library of testpip install -U pytest
# Import de ma fonction à tester
from streamlit_app import preprocess
from flair.data import Sentence
import tweepy as tp
from tweepy import OAuthHandler
import pandas as pd
import numpy as np

"""" test 1 : assert that the function preprocess returns the good sentence (with 3 words)"""
def test_preprocess():
    
    text = 'I like christmas'

    sentence = Sentence(preprocess(text))

    assert len(sentence) == 3

"""" test 2: assert that the preprocess function returns sentences of less than 280 words"""
def test_preprocess2():
    
    text = 'This is a very long sentence with more than 280 words - - -- - - - - - -- - - - - - - - - - - --  -- - - - - - - - -- - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - -- - - - - - -- - - - - - - - - - - --  -- - - - - - - - -- - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - -- - - - - - -- - - - - - - - - - - --  -- - - - - - - - -- - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - - - - - -- - - - - - - - - - - --  -- - - - - - - - -- - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -- - -- - - - - - -- - - - - - - - - - - --  -- - - - - - - - -- - - - - - - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -' 

    sentence = Sentence(preprocess(text))

    assert len(sentence) < 280

"""" test 3: assert that the preprocess function returns the allowed special characters"""
def test_preprocess3():
    
    text = 'This is a question with some allowed punctiations @?.' 

    phrase = Sentence(preprocess(text))

    assert ("@" in str(phrase)) 

"""" test 4: assert that the preprocess function does not return unauthorized special characters"""
def test_preprocess4():
    
    text = 'This is a question with a disallowed character ¤' 

    phrase = Sentence(preprocess(text))

    assert not("¤" in str(phrase))


""""We can't import the twitter_scrapper function in the test because it requires the action of a user on streamlit.
 We decide to rewrite it and simulate the action of a user who would have written the word "Worldcup" on the interface.
 We have set the number of tweets at 100."""

def get_twitter_scrap():
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
    no_of_tweets = 100 # change to unlimited

    #The number of tweets we want to retrieved from the search
    tweets = api.search_tweets('Worldcup', count=no_of_tweets)

    attributes_container = [[tweet.id, tweet.user.name, tweet.created_at, tweet.favorite_count, tweet.source,  tweet.text
                        , tweet.lang] for tweet in tweets]

    # On def les colonnes du dataframe
    columns = ["ID","User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet", "Lang"]
    #On créé un Df:
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
    tweets_df["Address"]= 'Worldcup'
    return tweets_df


"""" test 5 : assert that the function twitter_scrap returns the good dataset shape, with the good column names"""
@pytest.fixture
def tweets_df_columns():
    """"
    Get the column names of tweets_df
    """
    tweets_df_pydantic = get_twitter_scrap()
    tweets_df_pydantic_columns = tweets_df_pydantic.columns.to_list()
    return tweets_df_pydantic_columns

def test_tweets_df_columns(tweets_df_columns: callable):    
    tweets_df_schema = ["ID","User", "Date Created", "Number of Likes", "Source of Tweet", "Tweet", "Lang", "Address"]
    assert tweets_df_schema == tweets_df_columns


"""" test 6 : assert that the function twitter_scrap returns the right number of rows (set at 100)"""
@pytest.fixture
def tweets_df_rows():
    """"
    Get the number of rows of tweets_df
    """
    tweets_df_pydantic = get_twitter_scrap()
    tweets_df_pydantic_rows = len(tweets_df_pydantic.index)
    return tweets_df_pydantic_rows

def test_tweets_df_rows(tweets_df_rows: callable):
    assert tweets_df_rows == 100


"""" test 7 : assert that the function twitter_scrap contains no duplicated rows"""
@pytest.fixture
def tweets_df_duplicated():
    """"
    Get the duplicated rows of tweets_df
    """
    tweets_df_pydantic = get_twitter_scrap()
    tweets_df_pydantic_dup = tweets_df_pydantic[tweets_df_pydantic.duplicated()]
    return tweets_df_pydantic_dup

def test_tweets_df_duplicated(tweets_df_duplicated: callable):
    """"
    if the duplicated dataset is empty, there are no duplicated rows
    """
    assert tweets_df_duplicated.empty


""""
The type datetime64[ns, utc] is not available on numpy and pandas. 
We decide to remove this variable from the scrapping and to test the types for the other columns of the dataframe
"""

def get_twitter_scrap2():
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
    no_of_tweets = 100 # change to unlimited

    #The number of tweets we want to retrieved from the search
    tweets = api.search_tweets('Worldcup', count=no_of_tweets)

    attributes_container = [[tweet.id, tweet.user.name, tweet.favorite_count, tweet.source,  tweet.text
                        , tweet.lang] for tweet in tweets]

    # On def les colonnes du dataframe
    columns = ["ID","User", "Number of Likes", "Source of Tweet", "Tweet", "Lang"]
    #On créé un Df:
    tweets_df = pd.DataFrame(attributes_container, columns=columns)
    tweets_df["Address"]= 'Worldcup'
    return tweets_df


"""" test 8 : assert that the function twitter_scrap returns the good types of columns"""
@pytest.fixture
def tweets_df_types():
    """"
    Get the data types of tweets_df
    """
    tweets_df_pydantic = get_twitter_scrap2()
    tweets_df_pydantic_types = tweets_df_pydantic.dtypes.to_dict()

    return tweets_df_pydantic_types

def test_tweets_df_types(tweets_df_types: callable):
    """"
    Test the data type of tweets_df and the data type of the following database
    """
    expecttweets_datatypes = {'ID': np.dtype('int64'),
                   'User': np.dtype('O'),
                   'Number of Likes': np.dtype('int64'),
                   'Source of Tweet': np.dtype('O'),
                   'Tweet': np.dtype('O'),
                   'Lang': np.dtype('O'),
                   'Address': np.dtype('O')}
    assert tweets_df_types == expecttweets_datatypes      