# -*- coding: utf-8 -*-
"""sentiment_analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xzOYavbo5ojJNhgjg-HcHvxonTLT5muO
"""

import pandas as pd
import nltk

sentiment_data = pd.read_csv('/content/drive/MyDrive/Tweets.csv')

sentiment_data.head(10)

sentiment_data.info()

sentiment_data.shape

sentiment_df = sentiment_data.drop(sentiment_data[sentiment_data['airline_sentiment_confidence']<0.5].index, axis= 0)

sentiment_df.shape

sns.countplot(x='airline_sentiment', data=sentiment_df)

sns.boxplot(x='airline_sentiment', y='airline_sentiment_confidence', data=sentiment_df)

sns.distplot(sentiment_df['airline_sentiment_confidence'])

X = sentiment_df['text']
Y = sentiment_df['airline_sentiment']

from nltk.corpus import stopwords
nltk.download('stopwords')
import string
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

stop_words = stopwords.words('english')
punctuations = string.punctuation

import re
nltk.download('wordnet')

clean_data = []
for i in range(len(X)):
  text = re.sub('[^a-zA-Z]', ' ',X.iloc[i])
  text = text.lower().split()
  text = [lemmatizer.lemmatize(word) for word in text if (word not in stop_words) and (word not in punctuations)]
  text = ' '.join(text)
  clean_data.append(text)

clean_data

Y

# defining Sentiments:

sentiments = ['negative' , 'neutral', 'positive']
Y = Y.apply(lambda x: sentiments.index(x))
#Lets check Y that it has correctly changed or not:
Y.head()

from sklearn.feature_extraction.text import CountVectorizer

count_vectorizer = CountVectorizer(max_features = 5000, stop_words = ['virginamerica','united'])
X_fit = count_vectorizer.fit_transform(clean_data).toarray()

X_fit.shape

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
model = MultinomialNB()

X_train, X_test, Y_train, Y_test = train_test_split(X_fit,Y, test_size = 0.3)

model.fit(X_train,Y_train)

y_pred = model.predict(X_test)

from sklearn.metrics import classification_report

classification = classification_report(Y_test,y_pred)
print(classification)

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

# Assuming you have already trained your model and have y_pred (predicted labels)

# Calculate the confusion matrix
conf_matrix = confusion_matrix(Y_test, y_pred)

# Create a heatmap for better visualization
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues",
            xticklabels=model.classes_, yticklabels=model.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()