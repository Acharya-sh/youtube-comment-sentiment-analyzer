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

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud


# ---------------------------------------------------
# Output Directory
# ---------------------------------------------------

OUTPUT_DIR = os.path.join(
    "static",
    "generated"
)

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ---------------------------------------------------
# Pie Chart
# ---------------------------------------------------

def create_pie_chart(summary):
    """
    Creates the sentiment distribution pie chart.

    Zero-value sentiments are removed from the chart
    so that their labels do not overlap.
    """

    # Original order and colors
    labels = [
        "Positive",
        "Negative",
        "Neutral"
    ]

    sizes = [
        summary.get("positive", 0),
        summary.get("negative", 0),
        summary.get("neutral", 0)
    ]

    colors = [
        "#28a745",
        "#dc3545",
        "#ffc107"
    ]

    # ------------------------------------------------
    # Remove zero-value categories
    # ------------------------------------------------

    filtered_data = [
        (label, size, color)
        for label, size, color
        in zip(labels, sizes, colors)
        if size > 0
    ]

    filtered_labels = [
        item[0]
        for item in filtered_data
    ]

    filtered_sizes = [
        item[1]
        for item in filtered_data
    ]

    filtered_colors = [
        item[2]
        for item in filtered_data
    ]

    # ------------------------------------------------
    # Create Figure
    # ------------------------------------------------

    plt.figure(
        figsize=(6, 6)
    )

    # ------------------------------------------------
    # If sentiment data exists
    # ------------------------------------------------

    if filtered_sizes:

        plt.pie(
            filtered_sizes,
            labels=filtered_labels,
            colors=filtered_colors,
            autopct="%1.1f%%",
            startangle=140
        )

    # ------------------------------------------------
    # If there is no sentiment data
    # ------------------------------------------------

    else:

        plt.text(
            0.5,
            0.5,
            "No sentiment data available",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=14
        )

    plt.title(
        "Sentiment Distribution"
    )

    plt.axis("equal")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "pie_chart.png"
        ),
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------
# Word Cloud
# ---------------------------------------------------

def create_wordcloud(df):
    """
    Creates a word cloud from analyzed comments.
    """

    # Handle empty DataFrame
    if df is None or df.empty:

        plt.figure(
            figsize=(12, 6)
        )

        plt.text(
            0.5,
            0.5,
            "No comments available",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=18
        )

        plt.axis("off")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                OUTPUT_DIR,
                "wordcloud.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

        return

    # Make sure text column exists
    if "text" not in df.columns:

        return

    text = " ".join(
        df["text"].dropna().astype(str)
    )

    # Handle empty text
    if not text.strip():

        plt.figure(
            figsize=(12, 6)
        )

        plt.text(
            0.5,
            0.5,
            "No text available",
            horizontalalignment="center",
            verticalalignment="center",
            fontsize=18
        )

        plt.axis("off")

        plt.tight_layout()

        plt.savefig(
            os.path.join(
                OUTPUT_DIR,
                "wordcloud.png"
            ),
            bbox_inches="tight"
        )

        plt.close()

        return

    wc = WordCloud(
        width=900,
        height=500,
        background_color="white"
    )

    image = wc.generate(
        text
    )

    plt.figure(
        figsize=(12, 6)
    )

    plt.imshow(
        image,
        interpolation="bilinear"
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "wordcloud.png"
        ),
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------
# Top Words
# ---------------------------------------------------

def top_words(df, sentiment):
    """
    Returns the top words for a particular sentiment.
    """

    if df is None or df.empty:
        return [], []

    if "sentiment" not in df.columns:
        return [], []

    if "text" not in df.columns:
        return [], []

    comments = df[
        df["sentiment"] == sentiment
    ]["text"]

    # Remove empty comments
    comments = comments.dropna().astype(str)

    comments = comments[
        comments.str.strip() != ""
    ]

    if len(comments) == 0:
        return [], []

    try:

        vectorizer = CountVectorizer(
            stop_words="english",
            max_features=10
        )

        X = vectorizer.fit_transform(
            comments
        )

    except ValueError:

        # Happens when no usable words remain
        return [], []

    words = vectorizer.get_feature_names_out()

    counts = X.sum(
        axis=0
    ).A1

    return words, counts


# ---------------------------------------------------
# Positive Words Chart
# ---------------------------------------------------

def create_positive_chart(df):
    """
    Creates the Top Positive Words chart.
    """

    words, counts = top_words(
        df,
        "Positive"
    )

    if len(words) == 0:

        return

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(
        words,
        counts,
        color="green"
    )

    plt.xticks(
        rotation=45
    )

    plt.title(
        "Top Positive Words"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "positive_words.png"
        ),
        bbox_inches="tight"
    )

    plt.close()


# ---------------------------------------------------
# Negative Words Chart
# ---------------------------------------------------

def create_negative_chart(df):
    """
    Creates the Top Negative Words chart.
    """

    words, counts = top_words(
        df,
        "Negative"
    )

    if len(words) == 0:

        return

    plt.figure(
        figsize=(8, 5)
    )

    plt.bar(
        words,
        counts,
        color="red"
    )

    plt.xticks(
        rotation=45
    )

    plt.title(
        "Top Negative Words"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "negative_words.png"
        ),
        bbox_inches="tight"
    )

    plt.close()
