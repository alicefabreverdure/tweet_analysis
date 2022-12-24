import pytest # importing our library of testpip install -U pytest
# Import de ma fonction à tester
from streamlit_app import preprocess
from flair.data import Sentence

def test_preprocess():
    
    text = 'I like christmas'

    sentence = Sentence(preprocess(text))

    assert len(sentence) < 280

def test_preprocess2():
    
    text = 'This is a very long sentence with more than 280 characters ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------' 

    sentence = Sentence(preprocess(text))

    assert len(sentence) < 280


def test_preprocess3():
    
    text = 'This is a question with some allowed punctiations @?.' 

    phrase = Sentence(preprocess(text))

    assert ("@" in str(phrase)) 


def test_preprocess4():
    
    text = 'This is a question with a disallowed character ¤' 

    phrase = Sentence(preprocess(text))

    assert not("¤" in str(phrase))