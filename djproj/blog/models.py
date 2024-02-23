from django.db import models
from django.utils import timezone

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=250 )
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    #date
    publish = models.DateTimeField(Default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class  Meta:
        ordering = ['-publish']
        index=[
            models.Index(fields=['-publish'])
        ]
    def __str__(self):
        return self.title
    