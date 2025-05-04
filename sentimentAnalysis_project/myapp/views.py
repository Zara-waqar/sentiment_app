from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Sentiment
from django.contrib import messages
from datetime import datetime
import joblib
import numpy as np



def signup_view(request):
    if request.method == 'POST':
        username, email, password = request.POST['username'], request.POST['email'], request.POST['password']
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, 'Username or email already taken.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created! Log in now.')
            return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    return render(request, 'index.html')

# @login_required
# def view_sentences(request):
#     return render(request, 'view_sentences.html', {'sentences': Sentiment.objects.all()})

# Load the model and label encoder
model = joblib.load("ml_model/sentiment_model.joblib")
label_encoder = joblib.load("ml_model/label_encoder.joblib")

# Load GloVe embeddings
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

# Convert sentence to vector
def sentence_to_vector(sentence):
    words = sentence.lower().split()
    vectors = [glove_embeddings[word] for word in words if word in glove_embeddings]
    return np.mean(vectors, axis=0) if vectors else np.zeros(100)

# Predict sentiment
def predict_sentiment(sentence):
    vec = sentence_to_vector(sentence).reshape(1, -1)
    pred = model.predict(vec)
    label = label_encoder.inverse_transform(pred)[0]
    return label

@login_required
def create_sentence(request):
    if request.method == 'POST':
        sentence = request.POST.get('sentence')
        if sentence:
            try:
                sentiment = predict_sentiment(sentence)
                # Create the sentiment object and link the user
                Sentiment.objects.create(
                    sentence=sentence,
                    sentiment=sentiment,
                    user=request.user  # This will link the current logged-in user
                )
                messages.success(request, "Sentence saved successfully!")
                return redirect('home')  # Redirect after form submission

            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
                return redirect('create_sentence')  # Stay on the same page for error

    sentences = Sentiment.objects.all()
    return render(request, 'create_sentence.html', {'sentences': sentences})
@login_required
def update_sentence(request, id):
    sentence = get_object_or_404(Sentiment, id=id, user=request.user)
    if request.method == 'POST':
        sentence.sentence, sentence.sentiment = request.POST['sentence'], request.POST['sentiment']
        sentence.save()
    return render(request, 'update_sentence.html', {'sentence': sentence})
    return redirect('create_sentence')


@login_required
def delete_sentence(request, id):
    get_object_or_404(Sentiment, id=id, user=request.user).delete()
    return redirect('create_sentence')
