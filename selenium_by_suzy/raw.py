import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver



driver = webdriver.PhantomJS(r'C:\\Studying\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.implicitly_wait(2)
df = pd.read_csv('160749_after.csv', encoding='CP949')
total_list = []
cnt=0
for idn in df['nicknum'].values[2400:3200]:
    url = 'http://movie.naver.com/movie/point/af/list.nhn?st=nickname&target=after&sword='+str(idn)+'&page=1'
    driver.get(url)
    html = driver.page_source
    cnt += 1

    soup = BeautifulSoup(html,'html5lib')
    NumofComment = int(soup.find('strong','c_88 fs_11').text)
    NumofPage = int(NumofComment//10 if NumofComment//10==1 else (NumofComment//10)+1)
    driver2 = webdriver.PhantomJS(r'C:\\Studying\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    driver2.implicitly_wait(2)
    datef = re.compile('\d{2}\.\d{2}\.\d{2}')

    for page in range(NumofPage):
        url2 = 'http://movie.naver.com/movie/point/af/list.nhn?st=nickname&target=after&sword='\
               +str(idn)+'&page='+str(page+1)
        driver2.get(url2)
        html2 = driver2.page_source

        soup2 = BeautifulSoup(html2,'html5lib')

        tbody = soup2.find('tbody')
        trs = tbody.find_all('tr')

        table = [[user.find('td','ac num').text,
                  user.find('td','point').text,
                  user.find('a','movie').text,
                  re.sub('[\n\t]|신고|'+str(user.find('a','movie').text),'',user.find('td','title').text),
                str(idn),
                user.find('a','author').text,
                datef.findall(user.text)[0]]
                for user in trs]
        total_list.extend(table)
    driver2.close()
    print("%dth process" %cnt)

df_classnick = pd.DataFrame(data=total_list, columns=['commentnum','rate', 'movie', 'comment', 'nicknum', 'nick','date'])

df_classnick.to_csv('ReviewByNick.csv')#파일명 변경 순서대로 1,2,3,4,5..
driver.close()
