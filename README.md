# 699-capstone

## Table of Contents

1. [Project Overview](#project-overview) 
2. [Data Collection](https://github.com/rlieu/699-capstone/tree/main/api#readme)
3. [Data Preparation / Exploration](https://github.com/rlieu/699-capstone/blob/main/Exploring%20the%20whole%20dataset.ipynb)
4. [Sentiment Analysis](https://github.com/rlieu/699-capstone/blob/main/Sentiment%20Analysis.ipynb)
5. [Topic Modeling](https://github.com/rlieu/699-capstone/blob/main/Topic_Modeling/Topic_Modeling.ipynb)

## Project Overview 

This project examines Reddit posts from work-related communities to 
reveal variations in sentiment and user engagement across different times 
and discussion types. By analyzing how discussion moods shift throughout 
the day, week, and month, identifying the topics or flairs that generate the 
most interaction within subreddits, and comparing the interplay between 
post sentiment and user engagement, we aim to highlight the underlying 
patterns of online interactions. This effort seeks to provide insights into the 
dynamics of digital communities, enhancing our understanding of what 
influences discourse in online spaces.

## Data

This study leverages a dataset comprising posts from career-related 
subreddits, collected in March 2024. The dataset encapsulates a wide array 
of user-generated content, including queries about career advice, resume 
feedback, and job market discussions, amounting to a total of 7862 entries. 
Each entry is rich with information, such as the text of the post, the 
sentiment score derived from textual analysis, engagement metrics 
(including the number of comments and upvote ratio), and temporal data 
(time of posting, day of the week, and month) which transformed from the 
“created_utc” feature. This timely collection provides a snapshot of the 
current sentiments, concerns, and discussions within the job-seeking 
community, offering a unique lens through which to examine the prevailing 
trends and moods of the job market.

## Running Jupyter Notebooks

### Environment Steup (venv)

Activate virtual environment from project root

`source .venv/bin/activate`

Install required packages

`pip3 install -r requirements.txt`

Files with the `.ipynb` extension can now be run using the venv kernel


## Resources

### Reddit API

This project uses the [reddit API](https://www.reddit.com/dev/api/) to collect post data related to jobs/careers. 

### PostgreSQL Database (RDS) 

This project uses [postgres](https://www.postgresql.org/) running on [AWS RDS](https://aws.amazon.com/rds/) to store collected post data. 

### Flask 

This project is configured to use [Flask](https://flask.palletsprojects.com/en/3.0.x/) to serve collected post data through HTTP REST endpoints. 
