import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

import json

data = None

# Example dataset
with open('data.json', 'r') as file:
    data = json.load(file)

df = pd.DataFrame(data)

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['label'], test_size=0.2, random_state=42)

# Convert text to TF-IDF features
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Encode labels
encoder = LabelEncoder()
y_train_encoded = encoder.fit_transform(y_train)
y_test_encoded = encoder.transform(y_test)

# Train a Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_tfidf, y_train_encoded)

# Predict on the test data
y_pred = model.predict(X_test_tfidf)

# Calculate accuracy
accuracy = accuracy_score(y_test_encoded, y_pred)
print(f"Accuracy: {accuracy}")

# Define the new text you want to classify
new_text = [" one chance now"]

# Preprocess the new text using the same TF-IDF vectorizer used during training
new_text_tfidf = vectorizer.transform(new_text)

# Use the trained model to predict the label for the new text
predicted_label_encoded = model.predict(new_text_tfidf)

# Decode the label back to its original form
predicted_label = encoder.inverse_transform(predicted_label_encoded)

# Print the predicted label
print(f"The predicted label for the new text is: {predicted_label[0]}")