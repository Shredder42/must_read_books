from pymongo import MongoClient
import pprint
import pandas as pd
import requests
import bs4 from BeautifulSoup
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
# OR (not sure which one, would like to try them out)
soup.find_all('table', "tablesList js-dataTooltip")[0]

# identify the elements that I want
soup.find_all('tr itemscope', '')[1].find('td', 'number').text # ranking
soup.find_all('tr itemscope', '')[1].find('a', 'bookTitle').text.rstrip() # book title
soup.find_all('tr itemscope', '')[1].find('a', 'bookTitle').a['href'] # link to book
soup.find_all('tr itemscope', '')[1].find('a', 'authorname').span.text.rstrip() # author
soup.find_all('tr itemscope', '')[1].find('span', 'minirating').text.rstrip() #rating
soup.find_all('tr itemscope', '')[1].find('span', 'list_book_votes_2657').text # score
soup.find_all('tr itemscope', "")[1].find('a', 'loading_link_778518').text.rstrip() # votes

# loop through the entries
b_title = []
author = []
ranking = []
rating = []
score = []
votes = []
links = []

for idx, book in enumerate(soup.find_all('tr itemscope', '')):
    b_title.append(book.find('a', 'bookTitle).text.rstrip())
    author.append(book.find('a', 'authorName').span.text.rstrip())
    ranking.append(book.find('td', 'number').text
    rating.append(book.find('span', 'minirating').text.rstrip())
    score.append(book.find('span', 'list_book_votes_2657').text)
    votes.append(book.find('a', 'loading_link_778518').text.rstrip())
    links.append(book.find('a', 'bookTitle').a['href'])


# Step 4: Go through pulled hyperlinks for more data

b_format = []
pg_cnt = []
release = []

for link in links:
    sub_page = requests.get(link)
    pages.insert_one({'link': links, 'html': sub_page.text})
    sub_soup = BeautifulSoup(sub_page.text, 'html.parser')


    #  this is skipping the item by item inspection - I may want to do that

    fmt = sub_soup.find('span', 'bookFormat').text
    pgs = sub_soup.find('span', 'numberOfPages').text
    rls = sub_soup.find('nobr', 'greyText').text.rstrip()

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
print(link)
print(b_format)
print(pg_cnt)
print(release)
print(df.head())
