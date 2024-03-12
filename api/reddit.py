import praw
import json
import pandas as pd

reddit = praw.Reddit(
    client_id="jOk3mZmCBzb_VEdk-EA8ag",
    client_secret="QtoVwxP-aTBPqydl35y7kt6D-ahMOA",
    user_agent="web:app.web.checkin-9add1:v1",
)

def writeOutput(fileName, data):
    outputFile = open(fileName, "w")
    outputFile.write(json.dumps(data, sort_keys = True))

def prawSubreddit(subName, limit=100):
    print("Collecting from /r/{}...".format(subName))
    subreddit = reddit.subreddit(subName)
    submissions = subreddit.hot(limit=limit)
    redditData = []

    for submission in submissions:
        keys = ['title', 'text', 'author', 'author_flair_text', 'clicked', 'created_utc', 'distinguished', 'edited', 'id', 'is_original_content', 'is_self', 'link_flair_template_id', 'link_flair_text', 'locked', 'name', 'num_comments', 'over_18', 'permalink', 'saved', 'score', 'spoiler', 'stickied', 'upvote_ratio', 'url']
        func = [submission.title, submission.selftext, str(submission.author), submission.author_flair_text, submission.clicked, submission.created_utc, submission.distinguished, submission.edited, submission.id, submission.is_original_content, submission.is_self, submission.link_flair_template_id, submission.link_flair_text, submission.locked, submission.name, submission.num_comments, submission.over_18, submission.permalink, submission.saved, submission.score, submission.spoiler, submission.stickied, submission.upvote_ratio, submission.url]
        redditData.append(dict(zip(keys,func)))

    print("Finished Collecting.")
    writeOutput("{}.json".format(subName),redditData)

# prawSubreddit("jobs")

def load_posts(name):
    return pd.read_json('{}.json'.format(name))
