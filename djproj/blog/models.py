from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from django_jalali.db import models as jmodels #not using now
from django.urls import reverse

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
