from flask import Flask, render_template, request
import joblib
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

app = Flask(__name__)

# Load trained AI model
model = joblib.load("phishing_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Suspicious phishing words
suspicious_words = [
    "login",
    "verify",
    "bank",
    "secure",
    "update",
    "free",
    "password",
    "alert",
    "prize"
]

# Detect suspicious keywords
def keyword_score(url):

    score = 0
    found = []

    for word in suspicious_words:

        if word in url.lower():

            score += 10
            found.append(word)

    return score, found

# Check suspicious domain
def domain_check(url):

    parsed = urlparse(url)

    domain = parsed.netloc

    if "-" in domain:
        return 20

    return 0

# Detect fake login forms
def fake_login_detection(url):

    try:

        response = requests.get(url, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        forms = soup.find_all("form")

        if len(forms) > 0:
            return 20

    except:
        return 0

    return 0

@app.route("/", methods=["GET", "POST"])

def home():

    result = None
    risk_score = 0
    found_keywords = []

    if request.method == "POST":

        url = request.form["url"]

        # AI prediction
        vectorized_url = vectorizer.transform([url])

        prediction = model.predict(vectorized_url)[0]

        if prediction == 1:

            result = "Phishing Website Detected"
            risk_score += 40

        else:

            result = "Legitimate Website"

        # Keyword analysis
        score, found = keyword_score(url)

        risk_score += score
        found_keywords = found

        # Domain analysis
        risk_score += domain_check(url)

        # Login page detection
        risk_score += fake_login_detection(url)

        # Limit score to 100
        if risk_score > 100:
            risk_score = 100

        return render_template(
            "index.html",
            result=result,
            risk_score=risk_score,
            keywords=found_keywords,
            url=url
        )

    return render_template("index.html")

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
