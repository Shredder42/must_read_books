import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_and_concatenate(path, low, high):

    '''
    takes in csv files the range of numbers at the end of the csv files and returns
    an appended data frame

    input:
        path - the file path with a number for each csv
        low - lowest path number
        high - highest path number

    output:
        concatenated dataframe
    '''

    df_list = []
    for i in range(low,high+1):
        df_list.append(pd.read_csv(path.format(i)))

    concated = pd.concat(df_list)

    return concated

# drop the Unnamed column
data = data.drop(columns=['Unnamed: 0'])


def split_cols_by_space(x):
    '''
    will be used with .apply to split out numbers from columns
    (could also do this with a lambda function)

    input:

    output:
        the desired numeric value from the column
    '''

    if x.split(' ')[0] == 'didn\'t':
        return x.split(' ')[3]

    elif x.split(' ')[0] == 'it':
        return x.split(' ')[3]

    elif x.split(' ')[0] == 'really':
        return x.split(' ')[3]

    elif x.split(' ')[0] == 'liked':
        return x.split(' ')[2]

    else:
        return x.split(' ')[0]


def split_cols_by_big_hyphen(x):
    '''
    will be used with .apply to split out the values of the rating variable
    targeting the number of ratings in the 2nd part of the variable

    input:

    output:
        the desired numeric value from the column

    '''
    return x.split(' — ')[1]


def split_back_number(x):
    '''
    will be used with .apply to split out numbers at the back of each data column
    (could also do this with a lambda function)
    this targets the score variable

    input:


    output:
        second value of a list which is the desired number
    '''

    return x.split(': ')[1]

def remove_commas(col_name):

    '''
    removes commas from a numeric column in a data frame
    e.g. 1,234 -> 1234

    input:
        dataframe column

    output:
        dataframe
    '''

    data[col_name] = data[col_name].str.replace(",","")

    return data

def make_numeric(col_name):

    '''
    converts a text column containing numbers to a numeric column

    input:
        dataframe column

    output:
        dataframe
    '''

    data[[col_name]] = data[[col_name]].apply(pd.to_numeric)

    return data


if __name__ == '__main__'
data = read_and_concatenate('data/book_data_{}.csv',1,21)

data.info()
data.describe()
data.head()
data.tail()

# splits out number from votes column
data['votes']= data.votes.apply(split_cols_by_space)

# splits out number and creates new rating column
data['rating_1'] = data.rating.apply(split_cols_by_space)

# splits out number of ratings from rating column and creates cnt_ratings column
data['cnt_ratings'] = data.rating.apply(split_cols_by_big_hyphen)
data['cnt_ratings'] = data.cnt_ratings.apply(split_cols_by_space)

# makes rating column just the rating value and drops rating_1
data['rating'] = data['rating_1']
data = data.drop(columns=['rating_1'])

# splits out number from score column
data['score'] = data.score.apply(split_back_number)

# columns to remove commas from
remove_commas('cnt_ratings')
remove_commas('votes')
remove_commas('score')

# columns to make numeric from text
make_numeric('rating')
make_numeric('cnt_ratings')
make_numeric('votes')
make_numeric('score')

# create indicator for has at least 10 ratings
data['sufficient_ratings'] = np.where((data['cnt_ratings'] >= 10), 1, 0)
# create indicator for has at least 2 votes
data['sufficient_votes'] = np.where((data['votes'] > 1), 1, 0)
# create indicator for has at least 10 ratings and at least 2 votes
data['sufficient_data'] = np.where((data['sufficient_ratings'] == 1) & (data['sufficient_votes'] ==1), 1, 0)

# add variable to divide the overall rankings in half
# this indicates the "high ranked" vs "low ranked" books
data['high_rank'] = np.where(data['rank'] < (len(data['rank']) / 2), 1, 0)

data.info()
data.describe()
data.head()
data.tail()

data.to_csv('data/data_set.csv', index=False)