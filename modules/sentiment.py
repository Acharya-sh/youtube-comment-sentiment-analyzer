"""
===========================================================
Sentiment Analysis Module
SocialPulse - Multi Platform Sentiment Analyzer
===========================================================

Features
--------
✔ Text Cleaning
✔ VADER Sentiment Analysis
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

    text = re.sub(r"http\S+", "", text)

    text = re.sub(r"www\S+", "", text)

    text = re.sub(r"@\w+", "", text)

    text = re.sub(r"#", "", text)

    text = text.strip()

    return text


# ---------------------------------------------------
# Analyze One Comment
# ---------------------------------------------------

def analyze_comment(text):

    text = clean_text(text)

    scores = sia.polarity_scores(text)

    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"

    elif compound <= -0.05:
        sentiment = "Negative"

    else:
        sentiment = "Neutral"

    return {

        "text": text,

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

    results = []

    for comment in comment_list:

        results.append(analyze_comment(comment))

    df = pd.DataFrame(results)

    return df


# ---------------------------------------------------
# Sentiment Summary
# ---------------------------------------------------

def sentiment_summary(df):

    positive = len(df[df["sentiment"] == "Positive"])

    negative = len(df[df["sentiment"] == "Negative"])

    neutral = len(df[df["sentiment"] == "Neutral"])

    total = len(df)

    summary = {

        "total": total,

        "positive": positive,

        "negative": negative,

        "neutral": neutral,

        "positive_percent": round((positive / total) * 100, 2) if total else 0,

        "negative_percent": round((negative / total) * 100, 2) if total else 0,

        "neutral_percent": round((neutral / total) * 100, 2) if total else 0

    }

    return summary