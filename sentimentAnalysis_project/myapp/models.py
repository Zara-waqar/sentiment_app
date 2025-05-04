from django.db import models
from django.contrib.auth.models import User # for linking the username
from django.utils.timezone import now
class Sentiment(models.Model):
    
    sentiment = models.CharField( max_length=50)
    sentence = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Links the sentence to a user

    def __str__(self):
        return f'{self.sentence} - {self.sentiment}'
