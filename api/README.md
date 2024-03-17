### Run from terminal

Ask team member for `.env` file
```
cd api
python3


# get hot posts from each subreddit

>>> from reddit import praw_subreddit_hot
>>> praw_subreddit_hot(["jobs", "careerguidance"])

# get top posts by [all, year, month, week, day, hour] from subreddit
>>> from reddit import praw_subreddit_top
>>> praw_subreddit_top("jobs", filter="all")

# get random posts from subreddit

# ~200/1000 were unique
>>> from reddit import praw_subreddit_random
>>> praw_subreddit_random("jobs", num_posts=100)

# get DataFrame of posts from json file

>>> from reddit import load_posts
>>> df = load_posts("jobs")

# query posts from psql database (RDS)
# returns tuple (post_id,title,text,author,created_utc,num_comments,url,score,upvote_ratio,subreddit)

>>> from reddit import get_saved_posts
>>> posts = get_saved_posts("jobs")
```

### Collect posts from subreddit stream

Note: currently retrieves duplicate posts due to null `id`
Additionally, quantity of posts streamed is insufficient 
```
# ssh into AWS EC2 instance and activate virtual env
. python3-virtualenv/bin/activate
cd api/
gunicorn -b 0.0.0.0:8000 'reddit:praw_subreddit_stream()'
```