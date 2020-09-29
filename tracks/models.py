from django.db import models

class Track(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
