from django.db import models
from .user import User
from .novel import Novel

class Review(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='reviews')
  content = models.TextField()
