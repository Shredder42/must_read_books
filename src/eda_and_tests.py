import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
# Make plots look nice
plt.style.use('ggplot')
import scipy.stats as stats

data = pd.read_csv('data/data_set.csv')

# split by high and low rank
high_rating = data[data['high_rank'] == 1]['rating']
low_rating = data[data['high_rank'] == 0]['rating']


# create "sufficient data" data set (10+ ratings and 2+ votes)
sufficient = data[(data['sufficient_data'] == 1)]
sufficient['high_rank'] = np.where(sufficient['rank'] < (len(sufficient['rank']) / 2), 1, 0)
sufficient_high_rating = sufficient[sufficient['high_rank'] == 1]['rating']
sufficient_low_rating = sufficient[sufficient['high_rank'] == 0]['rating']

data.to_csv('data/data_set_sufficient.csv', index=False)


# Hypothesis Tests

# test on overall data set
t, p = stats.ttest_ind(low_rating, high_rating, equal_var=False)

# test on "sufficient" data set
def welch_test_statistic(sample_1, sample_2):
    numerator = np.mean(sample_1) - np.mean(sample_2)
    denominator_sq = (np.var(sample_1) / len(sample_1)) + \
                        (np.var(sample_2) / len(sample_2))
    return numerator / np.sqrt(denominator_sq)

test_statistic = welch_test_statistic(sufficient_low_rating, sufficient_high_rating)

def welch_satterhwaithe_df(sample_1, sample_2):
    ss1 = len(sample_1)
    ss2 = len(sample_2)
    df = (
        ((np.var(sample_1)/ss1 + np.var(sample_2)/ss2)**(2.0)) /
        ((np.var(sample_1)/ss1)**(2.0)/(ss1 - 1) + (np.var(sample_2)/ss2)**(2.0)/(ss2 - 1))
    )
    return df

df = welch_satterhwaithe_df(sufficient_low_rating, sufficient_high_rating)

students = stats.t(df)

test_statistic = welch_test_statistic(sufficient_low_rating, sufficient_high_rating)

p_value = students.cdf(test_statistic) + (1-students.cdf(-test_statistic))


if __name__ == '__main__'

data.info()
data.describe()
data.head()
data.tail()

fig, ax = plt.subplots(figsize=(8,5))
ax.hist(data['rating'], bins=50)
ax.axvline(data['rating'].mean(), color='black', linestyle='--')
plt.title('All Ratings Histogram')
plt.xlabel('Ratings')
plt.ylabel('Frequency')
ax.text(2.1, 1220, 'Mean = 4.071', fontsize = 15)
plt.show()
plt.savefig('img/all_ratings_histogram')

# split by high and low rank

high_rating.mean()
low_rating.mean()

fig, axs = plt.subplots(2, figsize=(8,5))
fig.suptitle('Ratings by Rank Level')
axs[0].hist(low_rating, bins=50)
axs[0].axvline(low_rating.mean(), color='black', linestyle='--')
axs[0].set_title('Low Rank')
axs[0].text(3.1, 610, 'Mean = 4.072', fontsize = 10)
axs[0].set_xlim(0, 5)
axs[0].set_ylim(0, 800)
axs[1].hist(high_rating, bins=50)
axs[1].axvline(high_rating.mean(), color='black', linestyle='--')
axs[1].set_title('High Rank')
axs[1].text(3.1, 610, 'Mean = 4.069', fontsize = 10)
axs[1].set_xlabel('Rating')
axs[1].set_xlim(0, 5)
axs[1].set_ylim(0, 800)
plt.show()
plt.savefig('img/all_ratings_by_rank_histogram')

fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(data['rank'], data['rating'], color = 'red')
ax.axhline(4.071, color='blue', linestyle='--', label='Ratings Mean')
ax.set_title("Distribution of Rating by Rank")
ax.set_xlabel("Rank")
ax.set_ylabel("Rating")
ax.legend(loc='best' )
plt.show()
plt.savefig('img/scatter_rating_rank.png')

fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(data['score'], data['rating'], color = 'red')
ax.set_title("Distribution of Log Score by Rating")
ax.axhline(4.071, color='blue', linestyle='--', label='Ratings Mean')
ax.set_xlabel("Log of Score")
ax.set_ylabel("Rating")
ax.set_xscale('log')
ax.legend(loc='best')
plt.show()
plt.savefig('img/scatter_rating_score.png')


# Sufficient data - At least 10 ratings and at least 2 votes
sufficient.info()
sufficient.describe()
sufficient.head()
sufficient.tail()

fig, ax = plt.subplots(figsize=(8,5))
ax.hist(sufficient['rating'], bins=50, color = 'green')
ax.axvline(sufficient['rating'].mean(), color='black', linestyle='--')
plt.title('Ratings Histogram for Books with 2+ Votes and 10+ Ratings')
plt.xlabel('Ratings')
plt.ylabel('Frequency')
ax.text(3.05, 710, 'Mean = 4.064', fontsize = 15)
plt.show()
plt.savefig('img/sufficient_ratings_histogram.png')

fig, axs = plt.subplots(2, figsize=(8,5))
fig.suptitle('Ratings by Rank Level for Books with 2+ Votes and 10+ Ratings')
axs[0].hist(sufficient_low_rating, bins=50, color='green')
axs[0].axvline(sufficient_low_rating.mean(), color='black', linestyle='--')
axs[0].set_title('Low Rank')
axs[0].text(3.1, 410, 'Mean = 4.054', fontsize = 10)
axs[0].set_xlim(0, 5)
axs[0].set_ylim(0, 500)
axs[0].set_ylabel('Frequency')
axs[1].hist(sufficient_high_rating, bins=50, color='green')
axs[1].axvline(sufficient_high_rating.mean(), color='black', linestyle='--')
axs[1].set_title('High Rank')
axs[1].text(3.1, 410, 'Mean = 4.066', fontsize = 10)
axs[1].set_xlabel('Rating')
axs[1].set_ylabel('Frequency')
axs[1].set_xlim(0, 5)
axs[1].set_ylim(0, 500)
plt.savefig('img/sufficient_ratings_by_rank_histogram.png')

fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(sufficient['score'], sufficient['rating'], color = 'green')
ax.set_title("Distribution of Log Score by Rating for Books with 2+ Votes and 10+ Ratings")
ax.axhline(4.060, color='blue', linestyle='--', label='Ratings Mean')
ax.set_xlabel("Log of Score")
ax.set_ylabel("Rating")
ax.set_xscale('log')
ax.legend(loc='best')
plt.savefig('img/sufficient_scatter_rating_score.png')

# Hypothesis Tests

# Test on overall data set
print(t)
print(p)

# Test on the on the "sufficient" data set
print(test_statistic)
print(df)
print(p_value)

# Distribution of Welsh's Test Statistic Under the Null Hypothesis
x = np.linspace(-3, 3, num=250)

fig, ax = plt.subplots(1, figsize=(16, 3))
students = stats.t(df)
ax.plot(x, students.pdf(x), linewidth=2, label="Degree of Freedom: {:2.2f}".format(df), color='green')
ax.fill_between(x, students.pdf(x), where=(x < test_statistic), color="green", alpha=0.25)
ax.fill_between(x, students.pdf(x), where=(x > -test_statistic), color="green", alpha=0.25)
ax.legend()
ax.set_title("Distribution of Welsh's T-Statistic Under Hypothesis that Low Ranked Boooks are Rated the Same as Higher Ranked");
ax.set_xlabel('t-statistic')
ax.set_ylabel('Density')
# ax.text(-1.99, 0.14, 't = -1.71', fontsize = 10)
# ax.text(-1.99, 0.11, 'p = 0.09', fontsize = 10)
plt.show()
plt.savefig('img/2_sided_ttest_distribution.png')