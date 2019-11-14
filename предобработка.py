import pandas as pd
import re
import nltk
from nltk.stem.snowball import SnowballStemmer

df = pd.read_csv('annotated_german.csv')
#считали csv датасет

df['content'] = df['content'].str.lower()
#привели каждую строчку в столбце content к нижнему регистру

df['content']

df['content'] = df['content'].apply(lambda row: re.compile(r'(\W)\1+').sub(r'\1', str(row)))
df['content'] = df['content'].apply(lambda row: re.compile(r'[^\w\s]').sub(r' ', str(row)).strip())
#для каждой записи формируем регулярное выражение, с помощью которого уберем все знаки препинания,
#и повторяющиеся символы
#с помощью лямбда функций применяем это к каждой записи в столбце content

df['content']

df['content'] = df['content'].apply(lambda index: nltk.word_tokenize(index))
#производим токенизацию(разбитие строк на смысловые единицы).
#используем лямбда функцию, которая работает с каждой строкой content и возвращает список слов в эту строку

df['content']

df['content'] = df['content'].apply(lambda row: list(map(lambda index:SnowballStemmer(language='german').stem(index),row)))
#далее производим стэмминг. Внешняя лямбда берет строку, а внутрення лямбда работает с каждым словом в этой строке
#к каждому слову применяем SnowballStemmer, возвращаем полученные слова в эту же строку.