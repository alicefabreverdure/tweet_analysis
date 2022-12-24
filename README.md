# Twitter Sentiment Analysis

Projet réalisé dans le cadre du cours de Cloud Computing 2022.

In this project, we used streamlit in order to create an interface to predict the sentiments of the tweet. 
The prediction of the tweet's sentiments is made by training a model named 'modele.py'. 

We will describe here in details the steps that should be made for a perfect functionning of this application. 

## Plan

1. Application : Streamlit_app
2. Model: modele.py
3. Requirements
4. Test using pytest
5. Image and container: Dockerfile and command


### 1. The application

To create the streamlit interface from python we need to install/import the following libraries:
- datetime
- pandas
- streamlit
- flair (falir.models and flair.data)

To define the title, background, subheadder, caption and other characteristics please check the streamlit_app.py file.

for the model we used the 'TextClassifier' model from flair library.

for the preprocessing of the tweet we created a function:

'''
def preprocess(text):
    return ''.join([' ' + char + ' ' if char in punct else char for char in [char for char in re.sub(r'http\S+', 'http', text, flags=re.MULTILINE) if char in allowed_chars]])[:maxlen]
'''

to load the model:

'''
with st.spinner('Loading classification model...'):
    classifier = TextClassifier.load('model-saves/best-model.pt')
'''
and to predict with this model:

'''
with st.spinner('Predicting...'):
        classifier.predict(sentence)
'''

After this procedure,we show the predictions on the interface by labeling the tweet as positive or negative sentiment.

### 2. the model



### 3. the requirements

In order to run our model, we need several dependencies.(streamlit, flair ...)

therefor, we created 'requirements.txt' file. this file contains the libraries with their speicific version for this appplication to run.

To install these dependencies, run the following code: 

```
pip install -r requirements.txt
```

### 4. The test using pytest




### 5. The image and container

To dockerize the app, we need to create a docker file. (assuming that you already have docker desktop)

Thus, we create a file 'Dockerfile'.(Dockerfile is a text document that contains all the commands needed to assemble an image).
docker build images automatically by reading the instructions from this Dockerfile.

In our case, we used python:3.10.8 as base image (It is crucial that you update python and work with python3.10 version so the flair's library work porperly.
we created the work directory '/app' and copy the files in it.

we installed the requirements using 
'''
RUN pip install requirements.txt
'''

and finally we used executed the:

'''
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
'''

### BONUS: we put our container on dockerhub
follow the link: https://hub.docker.com/repository/docker/alicefabreverdure/tweet_analysis

in vscode we can: docker pull alicefabreverdure/tweet_analysis
