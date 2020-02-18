import pandas as pd
import numpy as np
import time
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score


df_FullHtml = pd.read_csv(path_to_csv, encoding='utf-8-sig')
df_FullHtml = shuffle(df_FullHtml)
df_FullHtml = df_FullHtml[df_FullHtml['title']!='none']
df_FullHtml = df_FullHtml[df_FullHtml['title']!='']
df_FullHtml = df_FullHtml[['category','title']].reset_index()

df_FullHtml = df_FullHtml[['category','title']]
df_FullHtml['title'] = df_FullHtml['title'].astype('str')
print(len(set(df_FullHtml['category'])))

df2 = df_FullHtml
df4 = df2
df2 = df4[df4['title'].str.split().str.len() > 50]
print(len(set(df2['category'])))

df3 = df2.groupby('category')['title'].apply(lambda row: ' '.join(row)).reset_index()

idf_vectorizer = TfidfVectorizer()
tf_idf_matrix_train = idf_vectorizer.fit_transform(df3['title'])
vectorizer = CountVectorizer()
onehot_matrix_train = vectorizer.fit_transform(df2['title'])
result_matrix_train = tf_idf_matrix_train * onehot_matrix_train.T

X = result_matrix_train.T.toarray()
y = df2['category'].to_list()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

logreg = LogisticRegression(solver='newton-cg', multi_class='multinomial')
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('ACCURACY :', accuracy_score(y_pred, y_test))
print('F1 :', f1_score(y_pred, y_test, average='macro'))
