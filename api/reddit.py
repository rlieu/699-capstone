import os
import praw
import json
import boto3
import pandas as pd
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

    return doc_key

def write_output(fileName, data):
    outputFile = open(fileName, "w")
    outputFile.write(json.dumps(data, sort_keys = True))

def praw_subreddit(subName, filter='all'):
    print("Collecting from /r/{}...".format(subName))
    subreddit = reddit.subreddit(subName)
    # submissions = subreddit.hot(limit=filter)
    submissions = subreddit.top(time_filter=filter)
    reddit_data = []

    for submission in submissions:
        keys = ['title', 'text', 'author', 'author_flair_text', 'clicked', 'created_utc', 'distinguished', 'edited', 'id', 'is_original_content', 'is_self', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'saved', 'score', 'spoiler', 'stickied', 'upvote_ratio', 'url']
        func = [submission.title, submission.selftext, str(submission.author), submission.author_flair_text, submission.clicked, submission.created_utc, submission.distinguished, submission.edited, submission.id, submission.is_original_content, submission.is_self, submission.locked, submission.name, submission.num_comments, submission.over_18, submission.permalink, submission.saved, submission.score, submission.spoiler, submission.stickied, submission.upvote_ratio, submission.url]
        reddit_data.append(dict(zip(keys,func)))

    print("Finished collecting {} posts.".format(len(reddit_data)))
    file_name = "{}_top_{}.json".format(subName, filter)
    write_output(file_name, reddit_data)
    upload_to_s3(file_name)

    return reddit_data

# prawSubreddit("jobs", limit=100)

def load_posts(name):
    return pd.read_json('./{}.json'.format(name))
