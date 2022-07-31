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
import time
import random


def get_comments(url):
    n = 0 
    _time = [3, 15, 16, 21, 25, 32]
    data = {}

    def _analyze(comment):
        try:
            user = comment.find('div', class_='sc-4c216d8d-0 fEHNUE').text
            comment = comment.find('div', class_='sc-175a4cfa-0 ecZeGY').text
        except AttributeError as err:
            print('\n!!', err)
            return

        if '系' in user:
            user = user.split(' ')[0]
        elif '原 PO - ' in user:
            user = user.split(' - ')[1]
        elif '這則留言已被刪除' in user:
            return

        comment_list = []

        if user in data:
            data.get(user).append(comment)

        else:
            comment_list.append(comment)
            data[user] = comment_list

    #　文章頁面初次可讀出留言部分
    re = requests.get(url)
    soup = BeautifulSoup(re.text, 'html.parser')
    f = open('1_.txt', 'w', encoding='UTF-8')
    f.write(str(soup))
    comments = soup.find_all('div', class_='sc-995d8868-1 sc-e4e61263-0 eENAcb fNULcP')
    if 'CAPTCHA' in soup.text:
        print('\nComments download error.\nPlease wait.\n')
        quit()
    elif '沒有這個頁面' in soup.text:
        print('無索引之頁面,請檢查文章ID')
        quit()
    for comment in comments:
        n += 1
        _analyze(comment)
    print('已處理B1~B'+str(n)+'留言')
    n += 1

    _error = 0
    while n:
        page_url = url + '/b/'+str(n)
        print('read : ', page_url)
        re = requests.get(page_url)
        soup = BeautifulSoup(re.text, 'html.parser')
        file = str(n)+'.txt'
        f = open(file, 'w', encoding='UTF-8')
        f.write(str(soup.prettify()))
        if '沒有這個頁面' in soup.text:
            _error += 1
            n += 1
            print('沒有這個頁面')
            if _error >= 3:
                print('已計算至最後一組留言')
                break
            continue
        elif 'CAPTCHA' in soup.text:
            print('讓Dcard休息一下吧!')
            time.sleep(n*17 % 31+70)
            continue
        _error = 0
        a = random.choice(_time)
        print('Please wait ' + str(a) + ' seconds...')
        time.sleep(a)
        comment = soup.find('div', class_='sc-ea34e8f5-0 kmovFs')
        _analyze(comment)
        n += 1

    return data


def paint_data(data):
    x = -350
    y = 250
    total = 0
    other = 0
    t.bgcolor("black")
    t.pencolor("white")
    t.pensize(7)
    t.penup()

    def print_(y, user, n):
        t.goto(x, y)
        w = user + '  ' + str(n)
        t.write(w, font=('Arial', 13, 'normal'))
        t.goto(x+170, y+10)
        t.pendown()
        t.forward(7*n)
        t.penup()

    for user in data:
        if '大學' in user:
            n = data[user]
            total += n
            print_(y, user, n)
            y -= 20
            if y < -150:
                x += 340
                y = 250
        else:
            other += 1
    if other > 1:
        w = '其他' + str(other)
        print_(y, '其他', other)
        total += other

    t.goto(-227, -260)
    t.pendown()
    f = url + '\nDcard--各校留言計數器(製作者: naiye130)'
    t.write(f, font=('Arial', 18, 'normal'))
    print('共計算'+str(total)+'留言')
    t.done()


if __name__ == '__main__':
    url = str('https://www.dcard.tw/f/relationship/p/' + input('請輸入文章ID : '))
    data = get_comments(url)
    for _ in data:
        data[_] = len(data[_])
    data = dict(sorted(data.items(), reverse=True, key=lambda x: x[1]))
    print('\n使用者學校(名稱) 留言數 排行: \n')
    for _ in data:
        print(_, data[_])
    paint_data(data)
