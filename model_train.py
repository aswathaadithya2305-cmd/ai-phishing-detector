import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

# Sample phishing dataset
data = {
    "url": [
        "http://secure-login-paypal.com",
        "https://google.com",
        "http://bank-verification-alert.com",
        "https://github.com",
        "http://free-money-win-prize.com",
        "https://openai.com",
        "http://update-your-bank-password.com",
        "https://amazon.in"
    ],

    "label": [1, 0, 1, 0, 1, 0, 1, 0]
}

# Create dataframe
df = pd.DataFrame(data)

X = df["url"]
y = df["label"]

# Convert text into vectors
vectorizer = TfidfVectorizer()

X_vectorized = vectorizer.fit_transform(X)

# Train ML model
model = MultinomialNB()

model.fit(X_vectorized, y)

# Save model
joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")
