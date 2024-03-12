```
cd api
python3

>>> from reddit import prawSubreddit
>>> prawSubreddit("jobs", limit=100)

>>> from reddit import load_posts
>>> df = load_posts("jobs")
```