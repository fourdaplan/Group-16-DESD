# /text_model/train.py

import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

# Example training data
texts = [
    "This is an example text",
    "Another example for training",
    "Machine learning is awesome",
    "Deep learning for text data",
    "Natural Language Processing is useful"
]
labels = [0, 1, 0, 0, 1]  # Example classes

# Vectorize text
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

# Train classifier
model = RandomForestClassifier()
model.fit(X, labels)

# Save both vectorizer and model
save_path = './model.pkl'
with open(save_path, 'wb') as f:
    pickle.dump((vectorizer, model), f)

print(f'Model saved to {save_path}')
