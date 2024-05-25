from typing import Iterable
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django_jalali.db import models as jmodels #not using now
from django.urls import reverse
from django_resized import ResizedImageField
from .others import *
from django.template.defaultfilters import slugify

# manager
class PublishManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# Create your models here.
class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF' , 'Draft'
        PUBLISHED = 'PB' , 'Published'
        REJECTED = 'RG' , 'Rejected'

    CATEGORY_CHOICES=(
        ('تکنولوژی','تکنولوژی'),
        ('برنامه نویسی','برنامه نویسی'),
        ('سایر','سایر'),
    )
    
    #relation
    author = models.ForeignKey(User , on_delete=models.CASCADE , related_name="user_posts", verbose_name='نویسنده') 
    #data field
    title = models.CharField(max_length=200,verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=250)
    #date
    publish = models.DateTimeField(default=timezone.now,verbose_name='تاریخ انتشار')# j at first of words is just for persion date and time
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #choice field
    status = models.CharField(max_length=225 , choices=Status.choices , default=Status.DRAFT,verbose_name='وضعیت')
    category=models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='سایر')
    readingtime = models.PositiveBigIntegerField()
    #custom manager
    objects = models.Manager()
    published = PublishManager()
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
            ]
            # verbose_name="وب"

    def __str__(self):
        return self.title

    def get_absolute_url(self): # for making canonical urls(The unique url of each post)
        return reverse('blog:post_detail',args=[self.id])
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def delete(self, *args, **kwargs):
       for img in self.images.all():
        storage, path=img.image_file.storage, img.image_file.path
        storage.delete(path)
       super().delete(*args, **kwargs)

    def author_full_name(self):
        return str(self.author)
    
    
# for forms
class  Ticket(models.Model):
    message = models.TextField(verbose_name='پیام')
    name = models.CharField(max_length=250 , verbose_name='نام ')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11,verbose_name='شماره تماس')
    subject = models.CharField(max_length=250, verbose_name= "موضوع")

    # class Meta:
        # verbose_name="تیکت"
        # verbose_name_plural="تیکت ها"

    def __str__(self):
        return self.subject


class Comment(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="comments", verbose_name='پست')
    name = models.CharField(max_length=250,verbose_name='نام')
    body = models.TextField(verbose_name='متن کامنت')
    created = models.DateTimeField(auto_now_add=True)   
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
            ]
        
    def __str__(self):
        return f"{self.name}:{self.post}"

#for image field

class Image(models.Model):
    post = models.ForeignKey(Post , on_delete=models.CASCADE , related_name="images", verbose_name='تصاویر')
    image_file=ResizedImageField(upload_to=upload_to_author_directory,max_length=500,size=[500, 300], quality=75, crop=['middle', 'center'])#<<upload_to_author_directory>> this function imported from others.py file
    title   = models.CharField(max_length=200,verbose_name='عنوان', null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']  
        indexes = [
            models.Index(fields=['created'])
        ]
    def delete(self, *args, **kwargs):
        storage, path=self.image_file.storage, self.image_file.path
        storage.delete(path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else str(self.image_file)
    
class Account(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    date_of_birth= models.DateTimeField(null=True, blank=True)
    bio= models.TextField(null=True, blank=True)
    photo=ResizedImageField(upload_to=upload_to_author_directory_account,null=True, blank=True)
    job=models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.user.username
    