### Run from terminal

```
cd api
python3

# get top posts by [all, year, month, week, day, hour] from subreddit
>>> from reddit import praw_subreddit_top
>>> praw_subreddit_top("jobs", filter="all")

# get random posts from subreddit
>>> from reddit import praw_subreddit_random
>>> praw_subreddit_random("jobs", num_posts=100)

# load posts
>>> from reddit import load_posts
>>> df = load_posts("jobs")
```

### Collect posts from subreddit stream
```
# ssh into AWS EC2 instance and activate virtual env
. .venv/bin/activate
cd api/
gunicorn -b 0.0.0.0:8000 'reddit:praw_subreddit_stream()'
```