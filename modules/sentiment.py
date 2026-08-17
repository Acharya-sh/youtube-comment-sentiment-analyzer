"""
===========================================================
Sentiment Analysis Module
SocialPulse - Multi Platform Sentiment Analyzer
===========================================================

Features
--------
✔ Text Cleaning
✔ VADER Sentiment Analysis
✔ Emoji-aware sentiment handling
✔ Positive / Neutral / Negative Classification
✔ Sentiment Score
✔ DataFrame Generation
✔ Sentiment Summary

Author : SocialPulse
"""

import re
import pandas as pd
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer


# ---------------------------------------------------
# Download Required Resources
# ---------------------------------------------------

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")


sia = SentimentIntensityAnalyzer()


# ---------------------------------------------------
# Clean Text
# ---------------------------------------------------

def clean_text(text):
    """
    Cleans unnecessary URLs, mentions and extra spaces.
    """

    if text is None:
        return ""

    text = str(text)

    # Remove URLs
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"www\S+", "", text)

    # Remove @mentions
    text = re.sub(r"@\w+", "", text)

    # Remove # symbol but keep the actual word
    text = re.sub(r"#", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------
# Emoji Sentiment
# ---------------------------------------------------

def emoji_sentiment(text):
    """
    Detects common sentiment-related emojis.

    Returns:
        1  -> Positive
       -1  -> Negative
        0  -> No strong emoji sentiment
    """

    positive_emojis = [
        "❤️",
        "❤",
        "♥️",
        "♥",
        "😊",
        "😄",
        "😁",
        "😂",
        "🤣",
        "😍",
        "🥰",
        "😘",
        "👍",
        "👏",
        "🙌",
        "✨",
        "🔥",
        "💯",
        "🎉",
        "😎"
    ]

    negative_emojis = [
        "😡",
        "😠",
        "🤬",
        "😞",
        "😔",
        "😢",
        "😭",
        "😩",
        "😫",
        "👎",
        "💔",
        "🤮",
        "😱"
    ]

    for emoji in positive_emojis:
        if emoji in text:
            return 1

    for emoji in negative_emojis:
        if emoji in text:
            return -1

    return 0


# ---------------------------------------------------
# Analyze One Comment
# ---------------------------------------------------

def analyze_comment(text):
    """
    Analyze the sentiment of a single comment.

    VADER is used as the primary sentiment analyzer,
    with additional handling for emoji-only and
    very short comments.
    """

    original_text = "" if text is None else str(text)

    cleaned = clean_text(original_text)

    # Get emoji sentiment before removing anything
    emoji_score = emoji_sentiment(original_text)

    # VADER analysis
    scores = sia.polarity_scores(original_text)

    compound = scores["compound"]

    # ------------------------------------------------
    # Handle emoji-only comments
    # ------------------------------------------------

    if not cleaned:

        if emoji_score > 0:
            sentiment = "Positive"

        elif emoji_score < 0:
            sentiment = "Negative"

        else:
            sentiment = "Neutral"

    else:

        # ------------------------------------------------
        # VADER classification
        # ------------------------------------------------

        if compound >= 0.05:
            sentiment = "Positive"

        elif compound <= -0.05:
            sentiment = "Negative"

        else:

            # ------------------------------------------------
            # Emoji fallback
            # ------------------------------------------------

            if emoji_score > 0:
                sentiment = "Positive"

            elif emoji_score < 0:
                sentiment = "Negative"

            else:
                sentiment = "Neutral"

    return {

        "text": cleaned,

        "positive": scores["pos"],

        "negative": scores["neg"],

        "neutral": scores["neu"],

        "compound": compound,

        "sentiment": sentiment

    }


# ---------------------------------------------------
# Analyze Complete List
# ---------------------------------------------------

def analyze_comments(comment_list):
    """
    Analyze all comments and return a DataFrame.
    """

    results = []

    if not comment_list:
        return pd.DataFrame(
            columns=[
                "text",
                "positive",
                "negative",
                "neutral",
                "compound",
                "sentiment"
            ]
        )

    for comment in comment_list:

        result = analyze_comment(comment)

        results.append(result)

    df = pd.DataFrame(results)

    return df


# ---------------------------------------------------
# Sentiment Summary
# ---------------------------------------------------

def sentiment_summary(df):
    """
    Generate Positive / Neutral / Negative summary.
    """

    if df is None or df.empty:

        return {

            "total": 0,

            "positive": 0,

            "negative": 0,

            "neutral": 0,

            "positive_percent": 0,

            "negative_percent": 0,

            "neutral_percent": 0

        }

    positive = len(
        df[df["sentiment"] == "Positive"]
    )

    negative = len(
        df[df["sentiment"] == "Negative"]
    )

    neutral = len(
        df[df["sentiment"] == "Neutral"]
    )

    total = len(df)

    summary = {

        "total": total,

        "positive": positive,

        "negative": negative,

        "neutral": neutral,

        "positive_percent": round(
            (positive / total) * 100,
            2
        ) if total else 0,

        "negative_percent": round(
            (negative / total) * 100,
            2
        ) if total else 0,

        "neutral_percent": round(
            (neutral / total) * 100,
            2
        ) if total else 0

    }

    return summary
