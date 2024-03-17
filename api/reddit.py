import os
import praw
import json
import boto3
import pandas as pd
import requests
from psycopg2 import connect
from psycopg2.extras import execute_values
from time import sleep

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

def get_submission_data_praw(submission, name=None):
    # keys = ['title', 'text', 'author', 'author_flair_text', 'clicked', 'created_utc', 'distinguished', 'edited', 'id', 'is_original_content', 'is_self', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'saved', 'score', 'spoiler', 'stickied', 'upvote_ratio', 'url']
    # func = [submission.title, submission.selftext, str(submission.author), submission.author_flair_text, submission.clicked, submission.created_utc, submission.distinguished, submission.edited, submission.id, submission.is_original_content, submission.is_self, submission.locked, submission.name, submission.num_comments, submission.over_18, submission.permalink, submission.saved, submission.score, submission.spoiler, submission.stickied, submission.upvote_ratio, submission.url]
    keys = ['post_id', 'title', 'text', 'author', 'created_utc', 'num_comments', 'url', 'score', 'upvote_ratio', 'subreddit']
    func = [submission.id, submission.title, json.dumps(submission.selftext), str(submission.author), submission.created_utc, submission.num_comments, submission.url, submission.score, submission.upvote_ratio, name]
    
    return dict(zip(keys,func))

def save_posts(file_name, data):
    write_output(file_name, data)
    print("Saved {} posts.".format(len(data)))

    return file_name

def praw_subreddit_top(name, filter='all'):
    print("Collecting from /r/{}...".format(name))
    subreddit = reddit.subreddit(name)
    submissions = subreddit.top(time_filter=filter)
    reddit_data = []

    for submission in submissions:
        reddit_data.append(get_submission_data_praw(submission))

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
        reddit_data.append(get_submission_data_praw(submission))

    file_name = "{}_random_{}.json".format(name, num_posts)
    save_posts(file_name, reddit_data)
    upload_to_s3(file_name)

    return reddit_data

def praw_subreddit_stream(name="jobs"):
    collected_ids = get_collected_ids(name)
    print(collected_ids)
    print("Collecting from /r/{}...".format(name))

    subreddit = reddit.subreddit(name)
    for submission in subreddit.stream.submissions():
        if submission.id and submission.id not in collected_ids:
            print(vars(submission))
            execute_create("jobs", get_submission_data_praw(submission))
            collected_ids[submission.id] = submission.title

def praw_subreddit_hot(names, limit=None):
    collected_ids = get_collected_ids()
    for name in names:
        print("Collecting from /r/{}...".format(name))
        subreddit = reddit.subreddit(name)
        submissions = subreddit.hot(limit=limit)
        reddit_data = []

        conn = get_connection()
        for submission in submissions:
            print(vars(submission))
            data = get_submission_data_praw(submission)
            reddit_data.append(data)
            create_transaction(conn, "jobs", data)
            collected_ids[submission.id] = submission.title

        file_name = "{}_hot_{}.json".format(name, len(reddit_data))
        save_posts(file_name, reddit_data)
        upload_to_s3(file_name)
        conn.commit()

    return collected_ids

def execute_create(table, data):
    conn = get_connection()

    columns = data.keys()
    print(columns)
    print(len(columns))
    
    # query = "INSERT INTO {} ({}) VALUES (%s) RETURNING id".format(table, ','.join(columns))
    query = "INSERT INTO jobs (post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
    values = [item for item in data.values()]
    print(values)
    print(len(values))

    conn.cursor().execute(query, values)
    # execute_values(conn.cursor(), query, values, fetch=True)
    conn.commit()

def create_transaction(conn, table, data):
    columns = data.keys()
    print(columns)
    print(len(columns))
    
    # query = "INSERT INTO {} ({}) VALUES (%s) RETURNING id".format(table, ','.join(columns))
    query = "INSERT INTO jobs (post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
    values = [item for item in data.values()]
    print(values)
    print(len(values))

    conn.cursor().execute(query, values)

def get_submission_data(submission, name="jobs"):
    keys = ['post_id', 'title', 'text', 'author', 'created_utc', 'num_comments', 'url', 'score', 'upvote_ratio', 'subreddit']
    func = [submission['id'], submission['title'], submission['selftext'], submission['author'], submission['created_utc'], submission['num_comments'], submission['url'], submission['score'], submission['upvote_ratio'], name]
    
    return dict(zip(keys,func))

def get_posts(name, conn, url, collected_ids, after_id=None):
    get_url = url if not after_id else url + "&after_id={}".format(after_id)
    res = requests.get(get_url, headers={'User-agent': os.environ.get("REDDIT_USER_AGENT")})
    response = res.json()
    print(response)
    sleep(1)
    data = response['data']

    if data:
        cursor = conn.cursor()
        for item in data['children']:
            submission = item['data']
            if submission['id'] and submission['id'] not in collected_ids:
                print(submission['title'])
                create_posts(cursor, get_submission_data(submission, name))
                collected_ids[submission['id']] = submission['title']

        conn.commit()
        after_id = after_id if after_id != None else data['after']
        if after_id:
            get_posts(name, conn, url, collected_ids, after_id)


def collect_subreddit_posts(name="jobs", limit=100):
    collected_ids = get_collected_ids(name)
    print(collected_ids)
    print("Collecting from /r/{}...".format(name))

    url = "https://www.reddit.com/r/{}/new.json?limit={}".format(name, limit)
    conn = get_connection()
    get_posts(name, conn, url, collected_ids)

def load_posts(name):
    return pd.read_json('./{}.json'.format(name))

def get_connection():
    return connect(
        host=os.environ.get("DB_HOST"),
        database="reddit",
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        port="5432"
    )

def create_posts(cursor, data):
    columns = data.keys()
    print(columns)
    print(len(columns))
    
    query = "INSERT INTO jobs (post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"
    values = [item for item in data.values()]
    print(values)
    print(len(values))

    cursor.execute(query, values)

def get_saved_posts(table="jobs"):
    cur = get_connection().cursor()
    
    query = "SELECT post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit FROM {}".format(table)
    cur.execute(query)
    saved_posts = [post for post in cur.fetchall()]

    return saved_posts

def get_saved_posts_df(table="jobs"):
    conn = get_connection()
    query = "SELECT post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit FROM {}".format(table)
    posts_df = pd.read_sql(query, conn)

    return posts_df
    
def get_collected_ids(name="jobs"):
    return {post[0]:post[1] for post in get_saved_posts(name)}

