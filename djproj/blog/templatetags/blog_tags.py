from django import template
from ..models import Post,Comment
from django.db.models import Count , Max , Min , Avg , Sum
from markdown import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

register=template.Library()#for useing sipmletag decorator

@register.simple_tag()
def total_posts():
    return Post.published.count()

@register.simple_tag()
def total_comments():
    return Comment.objects.filter(active=True).count()

@register.simple_tag()
def last_post_published():
    return Post.published.last().publish

@register.simple_tag
def most_popular_posts(count=4):
    return Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]

@register.simple_tag
def most_time_taken(count=4):
    return Post.published.all().order_by('-readingtime')[:count]

@register.simple_tag
def less_time_taken(count=4):
    return Post.published.all().order_by('readingtime')[:count]

#Inclusion_tag
@register.inclusion_tag("partials/latest_posts.html") #relative path to the html
def latest_posts(count=4): 
    l_posts=Post.published.order_by('-publish')[:count] #get the latest posts
    context={'l_posts':l_posts}
    return context

@register.inclusion_tag("partials/active_users.html")#
def active_users(count=4):
    users=User.objects.annotate(total_posts=Count('user_posts')).order_by('-total_posts')[:count]
    return {'users':users}

#template filter
@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.filter(name='sunsor')
def sunsor(text):
    args=['nima' , 'zare', 'shenma']
    for arg in args:
        if arg in text:
            s=len(arg)
            text = text.replace(arg,'*'*s)
    return mark_safe(text)