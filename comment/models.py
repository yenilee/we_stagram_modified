from django.db import models
from user.models import User

class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

