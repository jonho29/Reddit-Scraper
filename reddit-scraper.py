import praw
import pandas as pd
from textblob import TextBlob
import math
from praw.models import MoreComments

reddit = praw.Reddit(client_id = '5S2N2WEcToRHAg', 
                     client_secret = 'dF7fHhY-Z2eFm5bb76q-aPwo8BY',
                     user_agent = 'Reddit Scraper')

num_subs = int(input('Number of subreddits to scrape: '))
counter = 1
posts = []
num_comments = 0

while counter <= num_subs:
    sub_input = input('Subreddit ' + str(counter) + ' to scrape: ')
    category = input('Category (hot (default), new, rising, top, gilded, or random) to scrape: ')
    if category == 'top':
        time_per = input('Time period (hour, day, week, month, year, all): ')
    if category != 'random':
        limit_num = int(input('Number of posts to scrape: '))

    subreddit = reddit.subreddit(sub_input)

    if category == 'random':
        cat = subreddit.random()
        posts.append([cat.title, cat.score, cat.subreddit, cat.url])
    else:
        cat = subreddit.hot(limit = limit_num)
        if category == 'new':
            cat = subreddit.new(limit = limit_num)
        if category == 'rising':
            cat = subreddit.rising(limit = limit_num)
        if category == 'top':
            if time_per != ('hour' or 'day' or 'week' or 'month' or 'year' or 'all'):
                time_per = 'all'
            cat = subreddit.top(time_per, limit = limit_num)
        if category == 'gilded':
            cat = subreddit.gilded(limit = limit_num)

        for submission in cat:
            post_sentiment = 0
            if not submission.stickied:
                submission.comments.replace_more(limit = 0)
                for comment in submission.comments.list():
                    blob = TextBlob(comment.body)
                    comment_sentiment = blob.sentiment.polarity
                    post_sentiment += comment_sentiment
                    num_comments += 1
                posts.append([submission.title, submission.score, submission.subreddit, submission.url, math.floor(post_sentiment / num_comments * 100)])

    counter += 1

posts = pd.DataFrame(posts, columns = ['Title', 'Score', 'Subreddit', 'URL', 'Submission Sentiment'])
posts.to_csv('/Users/jonho/Python/EE 551 Final Project/CSV Files/' + sub_input + '_' + category + '.csv')