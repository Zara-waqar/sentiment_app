import joblib
import numpy as np

# Load model and encoder
model = joblib.load("ml_model/sentiment_model.joblib")
label_encoder = joblib.load("ml_model/label_encoder.joblib")

# Load GloVe
def load_glove(path='ml_model/glove.6B.100d.txt'):
    embeddings = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split()
            word = parts[0]
            vector = np.array(parts[1:], dtype='float32')
            embeddings[word] = vector
    return embeddings

glove_embeddings = load_glove()

# Preprocess and vectorize
def sentence_to_vector(sentence):
    words = sentence.lower().split()
    vectors = [glove_embeddings[word] for word in words if word in glove_embeddings]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)

def predict_sentiment(sentence):
    vec = sentence_to_vector(sentence).reshape(1, -1)
    pred = model.predict(vec)
    label = label_encoder.inverse_transform(pred)[0]
    return label
