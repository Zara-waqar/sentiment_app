from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Sentiment
from django.contrib import messages
from .models import Sentiment
from predict import predict_sentiment 


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


@login_required
def create_sentence(request):
    if request.method == 'POST':
        sentence_text = request.POST['sentence']
        predicted_sentiment = predict_sentiment(sentence_text)
        Sentiment.objects.create(
            sentence=sentence_text,
            sentiment=predicted_sentiment,
            user=request.user
        )
        return redirect('create_sentence')  # or 'home' if you prefer
    sentences = Sentiment.objects.all().order_by('-created_at')
    return render(request, 'create_sentence.html', {'sentences': sentences})
@login_required
def update_sentence(request,id):
    sentence = get_object_or_404(Sentiment, id=id)
    
    if request.method == "POST":
        updated_text = request.POST.get('sentence')
        sentence.sentence = updated_text

        # Re-analyze sentiment
        predicted_sentiment = predict_sentiment(updated_text)
        sentence.sentiment = predicted_sentiment

        sentence.save()
        return redirect('create_sentence')  # or whatever your URL name is

    return render(request, 'update_sentence.html', {'sentence': sentence})

@login_required
def delete_sentence(request, id):
    get_object_or_404(Sentiment, id=id, user=request.user).delete()
    return redirect('create_sentence')
