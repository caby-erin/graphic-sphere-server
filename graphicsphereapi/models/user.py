from django.db import models

class User(models.Model):
    """Model for User table"""

    name = models.CharField(max_length=50)
    bio = models.CharField(max_length=250)
    uid = models.CharField(max_length=50)
