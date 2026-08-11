"""
===========================================================
YouTube Module
SocialPulse - Multi Platform Sentiment Analyzer
===========================================================

This module contains all YouTube related functions.

Features:
---------
✔ Search videos by keyword
✔ Fetch comments using video URL
✔ Fetch video information
✔ Return structured data

Author: SocialPulse
"""

import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import YOUTUBE_API_KEY


# ---------------------------------------------------
# Build YouTube API Object
# ---------------------------------------------------

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)


# ---------------------------------------------------
# Extract Video ID
# ---------------------------------------------------

def extract_video_id(url):
    """
    Extracts YouTube Video ID from different URL formats.
    """

    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be\/([a-zA-Z0-9_-]{11})",
        r"embed\/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)

        if match:
            return match.group(1)

    return None


# ---------------------------------------------------
# Fetch Video Details
# ---------------------------------------------------

def fetch_video_details(video_id):
    """
    Returns

    title
    channel
    views
    likes
    comments
    thumbnail
    published date
    """

    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    items = response.get("items")

    if not items:
        return None

    video = items[0]

    snippet = video["snippet"]
    stats = video["statistics"]

    details = {

        "video_id": video_id,

        "title": snippet.get("title"),

        "channel": snippet.get("channelTitle"),

        "published": snippet.get("publishedAt"),

        "thumbnail": snippet["thumbnails"]["high"]["url"],

        "views": int(stats.get("viewCount", 0)),

        "likes": int(stats.get("likeCount", 0)),

        "comments": int(stats.get("commentCount", 0))
    }

    return details


# ---------------------------------------------------
# Fetch Comments
# ---------------------------------------------------

def fetch_comments(video_id, limit=100):
    """
    Fetches top comments from YouTube.
    """

    comments = []

    next_page = None

    while len(comments) < limit:

        response = youtube.commentThreads().list(

            part="snippet",

            videoId=video_id,

            maxResults=100,

            textFormat="plainText",

            pageToken=next_page

        ).execute()

        for item in response.get("items", []):

            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]

            if len(comment.split()) > 3:
                comments.append(comment)

        next_page = response.get("nextPageToken")

        if not next_page:
            break

    return comments[:limit]


# ---------------------------------------------------
# Analyze Video From URL
# ---------------------------------------------------

def fetch_video_from_url(url):
    """
    Complete YouTube Fetch

    Returns

    {
        title,
        channel,
        likes,
        comments,
        views,
        thumbnail,
        comments_list
    }
    """

    video_id = extract_video_id(url)

    if video_id is None:
        raise Exception("Invalid YouTube URL")

    details = fetch_video_details(video_id)

    comments = fetch_comments(video_id)

    details["comments_list"] = comments

    return details


# ---------------------------------------------------
# Search Video By Keyword
# ---------------------------------------------------

def search_video(keyword):
    """
    Searches first suitable YouTube video.
    """

    search = youtube.search().list(

        q=keyword,

        part="snippet",

        type="video",

        maxResults=5

    ).execute()

    items = search.get("items")

    if not items:
        raise Exception("No videos found.")

    for item in items:

        video_id = item["id"]["videoId"]

        try:

            details = fetch_video_details(video_id)

            comments = fetch_comments(video_id)

            if len(comments) > 0:

                details["comments_list"] = comments

                return details

        except HttpError:

            continue

    raise Exception("No videos with comments found.")