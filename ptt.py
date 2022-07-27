import requests
from bs4 import BeautifulSoup

root_url = 'https://disp.cc/b/'

r = requests.get('https://disp.cc/b/PttHot')
soup = BeautifulSoup(r.text, 'html.parser')


# 找spen tag,然後需要有 titleColor 這個 class
spans = soup.find_all('span', class_='listTitle')  # L34 nowrap listTitle
for span in spans:
# 或將上2句改為 
# for span in soup.select('span.listTitle'):

    href = span.find('a').get('href')
    if href == 'PttHot/59l9':
        continue

    url = root_url + href
    title = span.text

    print(f'{title}\n{url}')
