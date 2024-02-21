from django.db import models
from .novel import Novel
from .genre import Genre

class NovelGenre(models.Model):
  novel = models.ForeignKey(Novel, on_delete=models.CASCADE, related_name='genres')
  genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name="novels")
