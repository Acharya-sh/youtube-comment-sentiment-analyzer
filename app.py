from flask import Flask, render_template, request, send_file
import pandas as pd
import os

from modules.youtube import fetch_video_from_url
from modules.reddit import fetch_post_from_url

from modules.sentiment import (
    analyze_comments,
    sentiment_summary
)

from modules.visualization import (
    create_pie_chart,
    create_wordcloud,
    create_positive_chart,
    create_negative_chart
)

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    url = request.form["url"]

    try:

        # -----------------------------
        # Detect Platform
        # -----------------------------

        if "youtube.com" in url or "youtu.be" in url:

            platform = "YouTube"

            data = fetch_video_from_url(url)

            title = data["title"]

            details = {
                "Channel": data["channel"],
                "Views": data["views"],
                "Likes": data["likes"],
                "Comments": data["comments"],
                "Published": data["published"]
            }

            thumbnail = data["thumbnail"]

            comments = data["comments_list"]

        elif "reddit.com" in url:

            platform = "Reddit"

            data = fetch_post_from_url(url)

            title = data["title"]

            details = {
                "Subreddit": data["subreddit"],
                "Author": data["author"],
                "Upvotes": data["score"],
                "Comments": data["comments_count"]
            }

            thumbnail = None

            comments = data["comments_list"]

        else:

            return render_template(
                "index.html",
                error="Unsupported URL."
            )

        # -----------------------------
        # Sentiment Analysis
        # -----------------------------

        df = analyze_comments(comments)

        summary = sentiment_summary(df)

        # -----------------------------
        # Charts
        # -----------------------------

        create_pie_chart(summary)

        create_wordcloud(df)

        create_positive_chart(df)

        create_negative_chart(df)

        # -----------------------------
        # CSV
        # -----------------------------

        csv_path = os.path.join(
            DOWNLOAD_FOLDER,
            "result.csv"
        )

        df.to_csv(csv_path, index=False)

        # -----------------------------
        # Top Comments
        # -----------------------------

        positive = df[df["sentiment"] == "Positive"].head(5)

        negative = df[df["sentiment"] == "Negative"].head(5)

        neutral = df[df["sentiment"] == "Neutral"].head(5)

        return render_template(

            "dashboard.html",

            platform=platform,

            title=title,

            thumbnail=thumbnail,

            details=details,

            summary=summary,

            positive_comments=positive.to_dict("records"),

            negative_comments=negative.to_dict("records"),

            neutral_comments=neutral.to_dict("records")

        )

    except Exception as e:

        return render_template(
            "index.html",
            error=str(e)
        )


@app.route("/download")
def download():

    return send_file(
        "downloads/result.csv",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)