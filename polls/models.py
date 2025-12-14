# polls/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=255)
    votes = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.option_text
