import os
import praw
import json
import boto3
import pandas as pd
from psycopg2 import connect
from psycopg2.extras import execute_values
# from time import sleep

reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"),
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent=os.environ.get("REDDIT_USER_AGENT"),
    ratelimit_seconds=300
)

def upload_to_s3(file_name):
    doc_key = "data/{}".format(file_name)

    s3 = boto3.resource('s3')
    s3.Bucket(os.environ.get("AWS_S3_BUCKET")).upload_file("./{}".format(file_name), doc_key)
    print("Uploaded {} to S3 bucket.".format(file_name))

    return doc_key

def write_output(fileName, data):
    outputFile = open(fileName, "w")
    outputFile.write(json.dumps(data, sort_keys = True))

def get_submission_data(submission):
    keys = ['title', 'text', 'author', 'author_flair_text', 'clicked', 'created_utc', 'distinguished', 'edited', 'id', 'is_original_content', 'is_self', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'saved', 'score', 'spoiler', 'stickied', 'upvote_ratio', 'url']
    func = [submission.title, submission.selftext, str(submission.author), submission.author_flair_text, submission.clicked, submission.created_utc, submission.distinguished, submission.edited, submission.id, submission.is_original_content, submission.is_self, submission.locked, submission.name, submission.num_comments, submission.over_18, submission.permalink, submission.saved, submission.score, submission.spoiler, submission.stickied, submission.upvote_ratio, submission.url]
    
    return dict(zip(keys,func))

def save_posts(file_name, data):
    write_output(file_name, data)
    print("Saved {} posts.".format(len(data)))

    return file_name

def praw_subreddit_hot(name, limit=None):
    print("Collecting from /r/{}...".format(name))
    subreddit = reddit.subreddit(name)
    submissions = subreddit.hot(limit=limit)
    reddit_data = []

    for submission in submissions:
        reddit_data.append(get_submission_data(submission))

    file_name = "{}_hot_{}.json".format(name, limit)
    save_posts(file_name, reddit_data)
    upload_to_s3(file_name)

    return reddit_data

def praw_subreddit_top(name, filter='all'):
    print("Collecting from /r/{}...".format(name))
    subreddit = reddit.subreddit(name)
    submissions = subreddit.top(time_filter=filter)
    reddit_data = []

    for submission in submissions:
        reddit_data.append(get_submission_data(submission))

    file_name = "{}_top_{}.json".format(name, filter)
    save_posts(file_name, reddit_data)
    upload_to_s3(file_name)

    return reddit_data

def praw_subreddit_random(name, num_posts=100):
    print("Collecting from /r/{}...".format(name))
    subreddit = reddit.subreddit(name)
    
    reddit_data = []
    for i in range(num_posts):
        submission = subreddit.random()
        reddit_data.append(get_submission_data(submission))

    file_name = "{}_random_{}.json".format(name, num_posts)
    save_posts(file_name, reddit_data)
    upload_to_s3(file_name)

    return reddit_data

def praw_subreddit_stream(name="jobs"):
    print("Collecting from /r/{}...".format(name))
    subreddit = reddit.subreddit(name)
    for submission in subreddit.stream.submissions():
        print(submission)
        execute_create("jobs", get_submission_data(submission))

def load_posts(name):
    return pd.read_json('./{}.json'.format(name))

def get_connection():
    return connect(
        host=os.environ.get("DB_HOST"),
        database="database-1",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        port="5432"
    )

def execute_create(table, data):
    conn = get_connection()

    data = [dict(sorted(x.items())) for x in data]
    columns = data[0].keys()
    print(columns)
    
    query = "INSERT INTO {} ({}) VALUES %s RETURNING id".format(table, ','.join(columns))
    values = [[str(value) if value else None for value in item.values()] for item in data]
    print(values)

    execute_values(conn.cursor(), query, values, fetch=True)
    conn.commit()