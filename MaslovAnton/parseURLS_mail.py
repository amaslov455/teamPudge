import pandas as pd
import urllib.request
import urllib.parse
import re
import bs4

a = 0

weburl = []
category = []
subcategory = []

for i in range(7702):
    url = 'https://top.mail.ru/Rating/All/Today/Visitors/'+str(i+1)+'.html'

    resp = urllib.request.urlopen(url)
    respData = resp.read()

    soup = bs4.BeautifulSoup(respData,'lxml')
    tbodies = soup.findAll('tbody',{'class':'ReportTable-TBody'})
    for tbody in tbodies:
        rows = tbody.findAll("tr",{"class":'ReportTable-TRow'})
        for row in rows:
            a += 1
            categ = row.findAll("a")[3].getText().split(' > ')
            weburl.append(row.findAll("a")[2].getText())
            category.append(categ[0])
            subcategory.append(categ[1])
            print(a)

d = {'url':weburl, 'category':category, 'subcategory':subcategory}
df = pd.DataFrame(data=d)

df.to_csv('D:\\mailTop100_parsed.csv', encoding='UTF-8-sig')