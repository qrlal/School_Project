import requests
from bs4 import BeautifulSoup
attr = {'class' : 'text-center'}
url = 'https://school.koreacharts.com/school/meals/B000023146/contents.html' # 급식 메뉴 가져올 사이트 url   새롬고: https://school.koreacharts.com/school/meals/B000023143/contents.html

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

title_data = soup.find_all('td', attrs = attr)
    
zeug = [x.get_text() for x in soup.find_all('td', attrs=attr)] # td태그 모든 내용 긁어오기

a=0
while a < len(zeug):
    zeug[a] = zeug[a].replace('\n', '<br>') #html에선 줄바꿈 == <br>
    
    a += 1

a=0
while a < len(zeug): # 들여쓰기 무필요
    zeug[a] = zeug[a].replace('\t', '')
    
    a += 1

with open('급식.txt', 'w', encoding='UTF-8') as f:
    f.write('')

i = 0
while i < len(zeug): # 쓸데없는 내용 다 지우고 메뉴만 불러오기

    if zeug[i] == '월요일' or zeug[i] == '화요일' or zeug[i] == '수요일' or zeug[i] == '목요일' or zeug[i] == '금요일':

        res = zeug[i+1]
        res1 = res[8:]
        res2 = res1[:-8]
        res2 = res2.replace('<br><br>', '<br>')
        with open('급식.txt','a',encoding='UTF-8') as f:
            f.write('"{0}",'.format(res2))

    i += 1

#읽기 모드
with open("급식.txt", "r",encoding='UTF-8') as f:
    # 파일 내용 읽어오기
    content = f.read()

# 맨 뒤의 글자 제거
content = content[:-1]

# 파일 쓰기 모드로 열어서 수정된 내용 저장
with open("급식.txt", "w",encoding='UTF-8') as f:
    f.write(content)



