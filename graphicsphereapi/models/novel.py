from django.db import models
from .user import User

class Novel(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=100)
  image_url = models.URLField()
  author = models.CharField(max_length = 100)
  illustrator = models.CharField(max_length = 100)
  description = models.TextField()
  rating = models.IntegerField(default=0)
