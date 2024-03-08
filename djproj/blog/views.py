from django.shortcuts import render
from django.http import HttpResponse,Http404
from .models import Post
# Create your views here.

def index(request):
    return HttpResponse("index")

def post_list(request):

    posts = Post.published.all()
    context={
        'posts':posts
        }
    return render(request,'blog/list.html',context)

def post_detail(request,id):
    try:
        post=Post.published.get(pk=id) # get the object with this id or raise an
    except:
        raise Http404("NO POST FOUND")
    
    context={
        'post':post
        }

    return render(request,"blog/detail.html",context)