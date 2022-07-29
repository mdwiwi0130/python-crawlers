import requests
from bs4 import BeautifulSoup

page_url = 'https://www.dcard.tw/f/relationship/p/239555645'
data = {}


f = open('html.txt', 'w', encoding='UTF-8')
re = requests.get(page_url)
soup = BeautifulSoup(re.text, 'html.parser')
f.write(str(soup))
comments = soup.find_all('div', class_='sc-995d8868-1 sc-e4e61263-0 eENAcb fNULcP')

for comment in comments:

    user = comment.find('div', class_='sc-e4c7c6d3-1 knaTFD').text
    comment = comment.find('div', class_='sc-8ec6ca7a-0 iuwIaf').text
    if '系' in user: 
        user = user.split(' ')[0]
    elif '這則留言已被刪除' in user:
        continue

    comment_list = []

    if user in data:
        data.get(user).append(comment)

    else:
        comment_list.append(comment)
        data[user] = comment_list

for _ in data:
    data[_] = len(data[_])
data = dict(sorted(data.items(), reverse=True, key=lambda x: x[1]))



if data == {}:
    print('\nMessage download error\n')
else:
    print('\n使用者名稱 留言數 排行: \n')
    for _ in data:
        print(_,data[_])
