from pymongo import MongoClient
import pprint
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json
import time

# Step 1: Requesting the URL

# How to handle every link in the GR list?
url = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=1'
r = requests.get(url)

r.status_code # printed below

# Step 2: Save into MongoDB

client = MongoClient()
db = client.goodreads

pages = db.must_read_books

pages.insert_one({'html': r.text})

# Step 3: Parse text to get data

soup = BeautifulSoup(r.text, 'html.parser')

# this will give me a big thing of whatever is in the entry for each book
soup.find_all('tr', "")[0]
entries = soup.find_all('tr', '')[0]


# identify the elements that I want
entries.find('td', 'number').text # ranking
entries.find('a', 'bookTitle').text.strip() # title
entries.find('a', 'bookTitle')['href'] # link to book
entries.find('a', 'authorName').text.rstrip() # author
entries.find('span', 'minirating').text.strip() # rating
entries.find('span', 'smallText uitext').find('a').text # score
entries.find('span', 'smallText uitext').find_all('a')[1].text # votes

# loop through the entries
b_title = []
author = []
ranking = []
rating = []
score = []
votes = []
links_pt2 = []

for idx, book in enumerate(soup.find_all('tr', '')):
    b_title.append(book.find('a', 'bookTitle').text.strip())
    author.append(book.find('a', 'authorName').text.strip())
    ranking.append(book.find('td', 'number').text)
    rating.append(book.find('span', 'minirating').text.strip())
    score.append(book.find('span', 'smallText uitext').find('a').text)
    votes.append(book.find('span', 'smallText uitext').find_all('a')[1].text)
    links_pt2.append(book.find('a', 'bookTitle')['href'])


# add full url links to go into each page

def combine_url_parts(lst):

    full_links = []
    for idx, link in enumerate(lst):
        link_lst = ['https://www.goodreads.com', lst[idx]]
        full_link = ''.join(link_lst)
        full_links.append(full_link)
    return full_links

# Step 4: Go through pulled hyperlinks for more data

b_format = []
pg_cnt = []
release = []

for link in links:
    sub_page = requests.get(link)
    pages.insert_one({'link': links, 'html': sub_page.text})
    sub_soup = BeautifulSoup(sub_page.text, 'html.parser')


    #  this is skipping the item by item inspection - I may want to do that

    fmt = sub_soup.find_all('div', 'row')[0].find_all('span')[0].text
    pgs = sub_soup.find_all('div', 'row')[0].find_all('span')[1].text
    rls = sub_soup.find_all('div', 'row')[1].find('nobr', 'greyText').text.strip()

    b_format.append(fmt)
    pg_cnt.append(pgs)
    release.append(rls)

    time.sleep(2)

# Step 5: Convert to Pandas data frame and .csv file

df = pd.DataFrame({'rank': ranking, 'title': b_title, 'author': author, 'format': b_format
                    'pages': pg_cnt, 'release_date': release, 'rating': rating, 'score': score
                    'votes': votes})

df.to_csv('bookreads_must_read_data.csv')



if __name__ == '__main__'
print(r.status code)
print(soup.prettify())
print(b_title)
print(author)
print(ranking)
print(rating)
print(score)
print(votes)
print(links_pt2)
print(combine_url_parts(links_pt2))
print(b_format)
print(pg_cnt)
print(release)
print(df.head())
