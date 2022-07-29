"""Dcard 各校留言計數器
本計數器非Dcard官方之程式

使用方法:
1.執行程式
2.輸入欲搜尋Dcard文章之ID(網址末端數字串)
3.開始計算留言
4.本程式將會產出:各校留言數量、搜尋文章的html檔

備註:
1.本計數器僅會計算文章留言,留言回復留言部分不計算
(以免對Dcard站台造成負擔)
2.本計數器計算依據為 使用者 名稱,若使用者名稱非校名將不予計算
3.若過頻繁執行本程式將會出現"Comments download error.",請讓Dcard站台喘口氣
4.若有留言被刪除本程式將會出現報錯訊息,請勿理會
5.本計數器為學術用途開發、使用,請遵守良好網路使用習慣

製作者: naiye130
"""

import requests
from bs4 import BeautifulSoup
import turtle as t


def get_comments(page_url):
    f = open('html.html', 'w', encoding='UTF-8')
    re = requests.get(page_url)
    soup = BeautifulSoup(re.text, 'html.parser')
    comments = soup.find_all('div', class_='sc-995d8868-1 sc-e4e61263-0 eENAcb fNULcP')
    f.write(str(comments))
    analyze_comments(comments)


def analyze_comments(comments):
    data = {}
    for comment in comments:
        try:
            user = comment.find('div', class_='sc-4c216d8d-0 fEHNUE').text
            comment = comment.find('div', class_='sc-175a4cfa-0 ecZeGY').text
        except AttributeError as err:
            print('\n!!',err,'!!\n',comment.text,'!!\n')

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
        print('\nComments download error.\nPlease wait.\n')
    else:
        print('\n使用者學校(名稱) 留言數 排行: \n')
        for _ in data:
            print(_,data[_])
        paint_data(data)

def paint_data(data):
    x = -350
    def print_(y,user,n):
        t.goto(x, y)
        w = user + '  ' +str(n)
        t.write(w, font=('Arial', 13, 'normal'))
        t.goto(x+170, y+8)
        t.pendown()
        t.forward(7*n)
        t.penup()
    
    y = 250
    other = 0
    t.bgcolor("black")
    t.pencolor("white")
    t.pensize(7)
    t.penup()
    for user in data:
        if '大學' in user :
            n =data[user]
            print_(y,user,n)
            y -= 20
            if y < -150:
                x += 340
                y = 250
        else:
            other += 1
    print_(y,'其他',other)
    w = '其他' + str(other)

    t.goto(-227, -260)
    t.pendown()
    f = page_url + '\nDcard--各校留言計數器(製作者: naiye130)'
    t.write(f, font=('Arial', 18, 'normal'))
    t.done()


if __name__ == '__main__':
    # page_url = 'https://www.dcard.tw/f/relationship/p/235807891'
    page_url = str('https://www.dcard.tw/f/relationship/p/' + input('請輸入文章ID : '))
    get_comments(page_url)
