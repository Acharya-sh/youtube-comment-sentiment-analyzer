"""
===========================================================
Reddit Module
SocialPulse - Multi Platform Sentiment Analyzer
===========================================================

Features
--------
✔ Analyze Reddit post using URL
✔ Search Reddit posts using keyword
✔ Fetch post details
✔ Fetch comments
"""

import praw

from config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT
)

# ---------------------------------------------------
# Reddit API Object
# ---------------------------------------------------

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


# ---------------------------------------------------
# Fetch Reddit Post Details
# ---------------------------------------------------

def fetch_post_details(submission):

    details = {

        "title": submission.title,

        "subreddit": submission.subreddit.display_name,

        "author": str(submission.author),

        "score": submission.score,

        "comments_count": submission.num_comments,

        "url": submission.url,

        "created": submission.created_utc

    }

    return details


# ---------------------------------------------------
# Fetch Comments
# ---------------------------------------------------

def fetch_comments(submission, limit=100):

    submission.comments.replace_more(limit=0)

    comments = []

    for comment in submission.comments.list():

        if hasattr(comment, "body"):

            if comment.body != "[deleted]" and len(comment.body.split()) > 3:

                comments.append(comment.body)

        if len(comments) >= limit:

            break

    return comments


# ---------------------------------------------------
# Analyze Reddit URL
# ---------------------------------------------------

def fetch_post_from_url(url):

    submission = reddit.submission(url=url)

    details = fetch_post_details(submission)

    details["comments_list"] = fetch_comments(submission)

    return details


# ---------------------------------------------------
# Search Reddit
# ---------------------------------------------------

def search_post(keyword):

    subreddit = reddit.subreddit("all")

    posts = subreddit.search(keyword, limit=10)

    for submission in posts:

        try:

            comments = fetch_comments(submission)

            if len(comments) > 0:

                details = fetch_post_details(submission)

                details["comments_list"] = comments

                return details

        except Exception:

            continue

    raise Exception("No suitable Reddit post found.")