from pymongo import MongoClient
import pprint
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

b_title = []
author = []
ranking = []
rating = []
score = []
votes = []
b_format = []
pg_cnt = []
release = []
new_release = []

iter = 0

for i in range(1,231):

    url = f'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page={i}'

#     new_url = url.split('=')
#     add_1 = int(new_url[1]) + 1
#     new_url[1] = str(add_1)
#     url = '='.join(new_url)

    iter += 1

    r = requests.get(url)

    client = MongoClient()
    db = client.goodreads_clean

    pages = db.must_read_books

    pages.insert_one({'html': r.text})

    soup = BeautifulSoup(r.text, 'html.parser')

    links_pt2 = []

    for idx, book in enumerate(soup.find_all('tr', '')):
        b_title.append(book.find('a', 'bookTitle').text.strip())
        author.append(book.find('a', 'authorName').text.strip())
        ranking.append(book.find('td', 'number').text)
        rating.append(book.find('span', 'minirating').text.strip())
        score.append(book.find('span', 'smallText uitext').find('a').text)
        votes.append(book.find('span', 'smallText uitext').find_all('a')[1].text)
        links_pt2.append(book.find('a', 'bookTitle')['href'])

    def combine_url_parts(lst):

        full_links = []
        for idx, link in enumerate(lst):
            link_lst = ['https://www.goodreads.com', lst[idx]]
            full_link = ''.join(link_lst)
            full_links.append(full_link)
        return full_links

    full_links = combine_url_parts(links_pt2)


    iter_sub = 0

    for link in full_links:

        iter_sub += 1

        sub_page = requests.get(link)

        sub_pages = db.must_read_books_sub

        sub_pages.insert_one({'link': link, 'html': sub_page.text})

        sub_soup = BeautifulSoup(sub_page.text, 'html.parser')

        sub_entries = sub_soup.find_all('div', 'row')

        try:
            fmt = sub_entries[0].find('span', {'itemprop': 'bookFormat'}).text # book format
        except:
            fmt = 'NA'

        try:
            pgs = sub_entries[0].find('span', {'itemprop':'numberOfPages'}).text # pages
        except:
            pgs = 'NA'

        try:
            rls = sub_entries[1].find('nobr', 'greyText').text.strip() # original publication
        except:
            rls = 'NA'

        try:
            n_rls = sub_entries[1].text.strip()
        except:
            n_rls = 'NA'

        b_format.append(fmt)
        pg_cnt.append(pgs)
        release.append(rls)
        new_release.append(n_rls)

        time.sleep(1)


df = pd.DataFrame({'rank': ranking, 'title': b_title, 'author': author, 'format': b_format,
                    'pages': pg_cnt, 'rating': rating, 'score': score,
                    'votes': votes, 'release_date': release, 'new_release_date': new_release})
df

df.to_csv('data/book_data.csv')