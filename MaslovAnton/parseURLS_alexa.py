import pandas as pd
import urllib.request
import urllib.parse
import re
import bs4
import requests
import concurrent.futures

arrCategory = []
arrSubcategory = []
arrLink = []

#Данные для авторизации на сайте через скрипт
login_data = {
    'csrf': 'new_csrf',
    'resource': 'https://www.alexa.com/pro/dashboard',
    'ip_address': '188.226.88.0',
    'email': 'amaslov455@gmail.com',
    'password': 'Anton77652'
}

#Спуск вглубь по категориям, возвращая ссылки на категории и колличество сайтов на более низком уровне
def GoDown(categurl):
    r = s.get(categurl)
    soup = bs4.BeautifulSoup(r.content,'lxml')
    uls = soup.findAll('ul',{'class':'subcategories'})
    numberOfURLs = 0
    array = []

    all_numbersOfURLs = soup.findAll('div',{'class':'alexa-pagination'})
    if len(all_numbersOfURLs) != 0:
        numberOfURLs = int(all_numbersOfURLs[-1].findAll('b')[-1].text)
    if len(uls) != 0:
        for ul in uls:
            lis = ul.findAll('li')
            for li in lis:
                newcategurl = urllib.parse.urljoin(categurl,li.a['href'])
                array.append(newcategurl)
    return array, numberOfURLs

#Главный алгоритм поиска сайтов, представляет из себя простой поиск в глубину с небольшими дополенениями
def DepthFirstSearch(linkurl):
    stack = [linkurl]
    visited = []
    
    while stack:
        print(len(arrLink), len(stack), print(stack[-1]))
        current = stack.pop()
        array, numberOfURLs = GoDown(current)
        if(len(array) != 0 and numberOfURLs == 500):
            for arr in array:
                if not arr in visited:
                    stack.append(arr)
            visited.append(current)
        else:
            ExtractDataToArrs(current)
            visited.append(current)

#Функция достает ссылку, категорию и подкатегорию каждого сайта на текущем уровне и кладет их в списки
def ExtractDataToArrs(url):
    oururl = 'https://www.alexa.com/topsites/category;'
    links = url.split('/')
    suburl = '/'+'/'.join(links[5:])
    newurl = oururl + str(0) + suburl
    r = s.get(newurl)
    soup = bs4.BeautifulSoup(r.content,'lxml')

    numberOfURLs = soup.findAll('div',{'class':'alexa-pagination'})
    if len(numberOfURLs) != 0:
        numrange = int(numberOfURLs[-1].findAll('b')[-1].text)
        numrange = -(-numrange//25)
        
        for i in range(numrange):
            urll = oururl + str(i) + suburl
            category = links[5]
            try:
                subcategory = links[6]
            except:
                pass
            r = s.get(urll)
            soup = bs4.BeautifulSoup(r.content,'lxml')
            sites = soup.findAll('div',{'class':'site-listing'})
            for site in sites:
                arrCategory.append(category)
                arrSubcategory.append(subcategory)
                arrLink.append('http://www.' + site.a.text.lower())

#Вход всего алгоритма, осуществляется авторизация на сайт, задается начальная вершина дерева поиска
#По окончании работы, списки со ссылками на сайты, их категориями и подкатегориями записываются в файл
if __name__ == '__main__':
    with requests.Session() as s:
        url = 'https://www.alexa.com/login'
        r = s.get(url)
        soup = bs4.BeautifulSoup(r.content,'lxml')
        foundcsrf = soup.find('input',attrs={'name':'csrf'})['value']
        login_data['csrf'] = foundcsrf
        r = s.post(url, data=login_data)
        
        url = 'https://www.alexa.com/topsites/category'
        cpuarray,_ = GoDown(url)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(DepthFirstSearch,cpuarray)

        d = {'url':arrLink, 'category':arrCategory, 'subcategory':arrSubcategory}
        df = pd.DataFrame(data=d)
        df.to_csv('D:\\alexa_russianV2.csv', encoding='UTF-8-sig')