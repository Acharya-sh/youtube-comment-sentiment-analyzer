# ==========================================
# CONFIGURATION FILE
# SocialPulse - Multi Platform Sentiment Analyzer
# ==========================================

import os
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# ----------------------------
# YouTube API Configuration
# ----------------------------

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# ----------------------------
# Reddit API Configuration
# ----------------------------

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")