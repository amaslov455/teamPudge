import socks
import socket
import time
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from pytrends.request import TrendReq
import random

#socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
#socket.socket = socks.socksocket

def append_new_line(file_name, text_to_append):

    with open(file_name, "a+") as file_object:
        file_object.seek(0)
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        file_object.write(text_to_append)

df = pd.read_csv('Organisation.csv', encoding='utf-8-sig')
df = df[['0']]
df = df.drop(0, 0)
df = df.reset_index(drop=True)
df = df.rename(columns={'0' : 'title'})

df1 = df.iloc[3300:3600]

all_titles = []
for text in df1['title']:
    all_titles.append(text)

print(len(all_titles))

#cv = CountVectorizer(all_titles, lowercase=False, ngram_range=(2,2))
#count_vector=cv.fit_transform(all_titles)

#print(len(cv.vocabulary_))

#bigrams = []

#for i in cv.vocabulary_:
    #bigrams.append(i)


count = 0

for word in all_titles:
    try:
        print(count)
        count +=1

        pytrend = TrendReq(hl='ru-RU', timeout=5)
        print(word)

        pytrend.build_payload(kw_list=[word], geo='RU', timeframe='2019-02-26 2020-02-26')
        interest_over_time_df = pytrend.interest_over_time()

        print('Start delay')
        time.sleep(random.randint(2,3))
        if len(interest_over_time_df) == 0:
            print('im in if')
            print('Not enough data')
            continue
        else:
            print('im in else')
            a = interest_over_time_df[word][0]
            for j in range(len(interest_over_time_df)):
                if interest_over_time_df[word][j] == 0:
                    continue
                else:
                    a = interest_over_time_df[word][j]
                    break
                        
            answer = (interest_over_time_df[word][len(interest_over_time_df)-1] - a) / a * 100
            print(answer)
            if answer >= 500:
                append_new_line('organisation.txt', word)
    except:
        continue