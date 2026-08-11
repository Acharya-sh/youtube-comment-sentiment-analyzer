"""
===========================================================
Visualization Module
SocialPulse - Multi Platform Sentiment Analyzer
===========================================================

Creates

✔ Pie Chart
✔ Word Cloud
✔ Top Positive Words
✔ Top Negative Words
"""

import os

OUTPUT_DIR = os.path.join("static", "generated")
os.makedirs(OUTPUT_DIR, exist_ok=True)

import matplotlib
matplotlib.use("Agg") 
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud



# ---------------------------------------------------
# Pie Chart
# ---------------------------------------------------

def create_pie_chart(summary):

    labels = ["Positive", "Negative", "Neutral"]

    sizes = [
        summary["positive"],
        summary["negative"],
        summary["neutral"]
    ]

    colors = ["#28a745", "#dc3545", "#ffc107"]

    plt.figure(figsize=(6,6))

    plt.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct="%1.1f%%",
        startangle=140
    )

    plt.title("Sentiment Distribution")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "pie_chart.png"))

    plt.close()


# ---------------------------------------------------
# Word Cloud
# ---------------------------------------------------

def create_wordcloud(df):

    text = " ".join(df["text"])

    wc = WordCloud(
        width=900,
        height=500,
        background_color="white"
    )

    image = wc.generate(text)

    plt.figure(figsize=(12,6))

    plt.imshow(image)

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "wordcloud.png"))

    plt.close()


# ---------------------------------------------------
# Top Words
# ---------------------------------------------------

def top_words(df, sentiment):

    comments = df[df["sentiment"] == sentiment]["text"]

    if len(comments) == 0:

        return [], []

    vectorizer = CountVectorizer(
        stop_words="english",
        max_features=10
    )

    X = vectorizer.fit_transform(comments)

    words = vectorizer.get_feature_names_out()

    counts = X.sum(axis=0).A1

    return words, counts


# ---------------------------------------------------
# Positive Words Chart
# ---------------------------------------------------

def create_positive_chart(df):

    words, counts = top_words(df, "Positive")

    if len(words) == 0:
        return

    plt.figure(figsize=(8,5))

    plt.bar(words, counts, color="green")

    plt.xticks(rotation=45)

    plt.title("Top Positive Words")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "positive_words.png"))

    plt.close()


# ---------------------------------------------------
# Negative Words Chart
# ---------------------------------------------------

def create_negative_chart(df):

    words, counts = top_words(df, "Negative")

    if len(words) == 0:
        return

    plt.figure(figsize=(8,5))

    plt.bar(words, counts, color="red")

    plt.xticks(rotation=45)

    plt.title("Top Negative Words")

    plt.tight_layout()

    plt.savefig(os.path.join(OUTPUT_DIR, "negative_words.png"))

    plt.close()