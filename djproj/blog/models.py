from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
        REJECTED = 'RG' , 'Rejected'    

    #relation
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_posts")
    #data field
    title = models.CharField(max_length=200)
    description = models.TextField()
    slug = models.SlugField(max_length=250)
    #date
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #choice field
    Status = models.CharField(max_length=225 , choices=Status.choices , default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [models.Index(fields=['-publish'])]

    def __str__(self):
        return self.title
    