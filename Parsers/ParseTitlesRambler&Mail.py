import requests
import time
import pandas as pd
import urllib3
from bs4 import BeautifulSoup as bs
from multiprocessing.dummy import Pool

def title_parser(url):
    headers = {
    'Accept' : '*/*',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    try:
        request = session.get(url, headers=headers, verify=False)
        if request.status_code == 200:
            soup = bs(request.content, 'html.parser', from_encoding='utf-8')
            if soup.find('title') != None:
                return soup.find('title').text
            else:
                return 'none'
        else:
            return 'none'
    except :
        print("Ошибка " + url)
        return 'none'

if __name__ == '__main__':

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    session = requests.Session()
    df = pd.read_csv(path_to_csv_file_with_url)
    df = df[['url','category','subcategory']]
    urls = df['url'].to_list()

    start_working_code = time.time()

    for i in range(len(df) // 1000):
        start_time = time.time()
        print(i)
        with Pool(8) as p:
            titles = p.map(title_parser, urls[1000*i:1000*(i+1)])
        
        df1 = df[1000*i:1000*(i+1)]
        df1['title'] = titles
        titles.clear()
        
        if i ==0:
            with open(path_to_file, 'a', encoding='utf-8-sig',newline='') as f:
                df1.to_csv(f, header=True)
        else:
            with open(path_to_file, 'a', encoding='utf-8-sig',newline='') as f:
                df1.to_csv(f, header=False)

        print(f"{(time.time() - start_time)} секунд")
    
    print('Last iteration')
    with Pool(8) as p:
        titles = p.map(title_parser, urls[len(df)-len(df)%1000:len(df)])
    
    df1 = df[len(df)-len(df)%1000:len(df)]
    df1['title'] = titles

    with open(path_to_file, 'a', encoding='utf-8-sig',newline='') as f:
                df1.to_csv(f, header=False)
    print(f"{(time.time() - start_working_code)} секунд")
