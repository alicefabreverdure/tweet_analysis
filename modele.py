## Creation d'un modele permettant de savoir si un tweet confere un sentiment positif ou negatif
## et à quelle niveau de confiance

# Load data
import pandas as pd

col_names = ['sentiment','id','date','query_string','user','text']
data_path = 'training.1600000.processed.noemoticon.csv'

tweet_data = pd.read_csv(data_path, header=None, names=col_names, encoding="ISO-8859-1").sample(frac=1) # .sample(frac=1) shuffles the data
tweet_data = tweet_data[['sentiment', 'text']] # Disregard other columns
print(tweet_data.head())

# Preprocess function
import re
allowed_chars = ' AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789~`!@#$%^&*()-=_+[]{}|;:",./<>?'
punct = '!?,.@#'
maxlen = 280

def preprocess(text):
    return ''.join([' ' + char + ' ' if char in punct else char for char in [char for char in re.sub(r'http\S+', 'http', text, flags=re.MULTILINE) if char in allowed_chars]])[:maxlen]

# Apply preprocessing
tweet_data['text'] = tweet_data['text'].apply(preprocess)

# Put __label__ in front of each sentiment
tweet_data['sentiment'] = '__label__' + tweet_data['sentiment'].astype(str)

# Save data
import os

# Create directory for saving data
data_dir = './processed-data'
if not os.path.isdir(data_dir):
    os.mkdir(data_dir)

# Save a percentage of the data
amount = 0.125

tweet_data.iloc[0:int(len(tweet_data)*0.8*amount)].to_csv(data_dir + '/train.csv', sep='\t', index=False, header=False)
tweet_data.iloc[int(len(tweet_data)*0.8*amount):int(len(tweet_data)*0.9*amount)].to_csv(data_dir + '/test.csv', sep='\t', index=False, header=False)
tweet_data.iloc[int(len(tweet_data)*0.9*amount):int(len(tweet_data)*1.0*amount)].to_csv(data_dir + '/dev.csv', sep='\t', index=False, header=False)
