import requests
import time
import pandas as pd
import urllib3
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool
import concurrent.futures

df = pd.read_csv(path_to_file_with_url)

def title_parser(url):
    headers = {
    'Accept' : '*/*',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    try:
        request = session.get(url, headers=headers, verify=False, timeout=10)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser', from_encoding='utf-8')
            [tag.decompose() for tag in soup("script")]
            [tag.decompose() for tag in soup("style")]
            
            title = soup.find('title').get_text()
            [tag.decompose() for tag in soup("title")]

            try:
                meta_tag = soup.find('meta', attrs={'name': 'description'})['content']
            except:
                meta_tag = ''
            arr = [' '.join(value.split()) for value in soup.get_text().splitlines() if value != '']
            arr = ' '.join(arr)
            return title, meta_tag, arr
        else:
            return 'none','none','none'
    except :
        print("Ошибка " + url)
        return 'none','none','none'

if __name__ == '__main__':

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()

    count = 0
    urls = df['url'].to_list()
    dflen = len(df)

    for i in range((dflen // 1000)+1):
        if i >= 0:
            start_time = time.time()
            print(i)
            df1 = df[1000*i:1000*(i+1)]

            with Pool(100) as p:
                titles, desc, content = zip(*p.map(title_parser, urls[1000*i:1000*(i+1)]))

            df1['title'] = list(titles)
            df1['description'] = list(desc)
            df1['content'] = list(content)
            
            try:
                if i == 0:
                    with open(path_to_file, 'w', encoding='utf-8-sig', newline='') as f:
                        df1.to_csv(f, header=True)
                else:
                    print('Start saving...')
                    with open(path_to_file, 'a', encoding='utf-8-sig', newline='') as f:
                        df1.to_csv(f, header=False)
            except:
                pass

            print(f"{(time.time() - start_time)} секунд")