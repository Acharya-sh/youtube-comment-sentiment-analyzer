# 🚀 SocialPulse - Multi-Platform Sentiment Analyzer

SocialPulse is a Flask-based web application that performs sentiment analysis on comments from **YouTube videos** and **Reddit posts**. It uses Natural Language Processing (NLP) techniques to classify comments as **Positive**, **Negative**, or **Neutral**, and presents the results through interactive visualizations.

---

## 📌 Features

- 🔍 Analyze YouTube video comments
- 💬 Analyze Reddit post comments
- 😊 Sentiment Classification (Positive, Negative, Neutral)
- 📊 Sentiment Distribution Pie Chart
- ☁️ Word Cloud Generation
- 📈 Top Positive & Negative Words
- 📥 Download analysis results as CSV
- 🌐 User-friendly web interface

---

## 🛠️ Tech Stack

### Frontend
- HTML
- CSS
- Bootstrap 5
- JavaScript

### Backend
- Python
- Flask

### NLP & Data Processing
- NLTK
- Scikit-learn
- Pandas
- NumPy

### Visualization
- Matplotlib
- WordCloud
- Plotly

### APIs
- YouTube Data API v3
- Reddit API (PRAW)

---

## 📂 Project Structure

```text
SocialPulse/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
├── modules/
│   ├── youtube.py
│   ├── reddit.py
│   ├── sentiment.py
│   └── visualization.py
│
├── templates/
├── static/
├── downloads/
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/youtube-comment-sentiment-analyzer.git
cd youtube-comment-sentiment-analyzer
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows

```bash
venv\Scripts\activate
```

Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env
YOUTUBE_API_KEY=YOUR_YOUTUBE_API_KEY

REDDIT_CLIENT_ID=YOUR_CLIENT_ID

REDDIT_CLIENT_SECRET=YOUR_CLIENT_SECRET

REDDIT_USER_AGENT=YOUR_USER_AGENT
```

---

## ▶️ Run the Project

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

---

## 📷 Screenshots

Add screenshots of:

- Home Page
- Dashboard
- Sentiment Pie Chart
- Word Cloud
- CSV Download

---

## 🌍 Live Demo

**Render Deployment**

https://youtube-comment-sentiment-analyzer-5ghn.onrender.com

---

## 📁 GitHub Repository

https://github.com/your-username/youtube-comment-sentiment-analyzer

---

## 📈 Future Improvements

- Support for Twitter/X
- Transformer-based sentiment analysis (BERT)
- Emotion Detection
- Multi-language Support
- User Authentication
- Dashboard History
- Database Integration

---

## 👨‍💻 Author

**Yash Acharya**

B.E. Artificial Intelligence & Machine Learning

---

## 📄 License

This project is developed for educational purposes as an NLP Mini Project.
