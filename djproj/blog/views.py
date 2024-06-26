from django.shortcuts import render,get_list_or_404 ,redirect , get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from .models import *
from .froms import *
from .others import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView,DeleteView #for class based views
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery ,SearchRank, TrigramSimilarity
from django.contrib.auth import authenticate, login, logout #for login
from django.db.models import Count
from django.views.generic import View

# Create your views here.
def index(request):
    return render(request , "blog/index.html" )
#>> ______________________________________________________________________________________________________________________________________
def post_list(request, category=None):
    if category is not None:
        posts=Post.published.filter(category=category)
    else:
        posts = Post.published.all()

    posts = Post.published.all()

    paginator = Paginator(posts, 4) #
    page_number = request.GET.get('page',1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        raise Http404("Sorry! That page does not exist.")# posts = paginator.page(paginator.num_pages) <we can use this insted that>
    except PageNotAnInteger:
        posts = paginator.page(1)
        
    context={
        'posts':posts,
        'category':category,
        }
    return render(request,'blog/list.html',context)
# _______________________________________________________________________________________________________________________________________

# its for class based views
# class PostListView(ListView):
#     # model=Post
#     queryset=Post.published.all()
#     context_object_name='posts'
#     paginate_by=5
#     template_name='blog/list.html'

# >> ________________________________________________________________________________________________________________
def post_detail(request,id):
    post= get_object_or_404(Post,id=id , status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True) # for comment
    form=Commentform() #for comment
    context={
        'post':post,
        'form':form, #for comment
        'comments':comments, #for comment
    }
    return render(request,"blog/detail.html",context)
# ________________________________________________________________________________________________________________
    # try:
    #     post=Post.published.get(pk=id) # get the object with this id or raise an
    # except:
    #     raise Http404("NO POST FOUND")
    
    # context={
    #     'post':post,
    #     'new_date' :datetime.datetime.now()
        
    #     }

    # return render(request,"blog/detail.html",context)
# ________________________________________________________________________________________________________________

# class PostDetailView(DeleteView):
#     model=Post
#     template_name='blog/detail.html'



 
def ticket(request):
    if request.method == "POST":
        form =TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ticket_obj = Ticket.objects.create()
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.phone = cd['phone']
            # ticket_obj.subject = cd['subject']
            # ticket_obj.save()                       #we can use the bottom line instead of these 7 lines

            Ticket.objects.create(message = cd['message'] ,name = cd['name'] , email = cd['email'] , phone = cd['phone'] , subject = cd['subject'] )
            return redirect('blog:index') # send user back to index page after submitting ticket
    else:
        form = TicketForm()
    return render(request,"forms/ticket.html" , {'form':form})


@require_POST
def post_comment(request , post_id):
    post = get_object_or_404(Post, id=post_id , status=Post.Status.PUBLISHED)
    comment=None
    form=Commentform(data=request.POST)
    if form.is_valid():
        comment=form.save(commit=False)
        comment.post = post
        comment.save()
    context={
        'post':post,
        'form':form,
        'comment':comment
        }
    return render(request , "forms/comment.html" , context)

def post_search(request):
    query=None
    results=[]
    if 'query' in request.GET:
        form=SearchForm(data=request.GET)
        if form.is_valid():
            query=form.cleaned_data['query']
            # results=Post.published.filter(Q(title__search=query) | Q(description__search=query))
            # search_query=SearchQuery(query)
            # search_vector=SearchVector('title', 'description')
            #
            results1=Post.published.annotate(similarity=TrigramSimilarity('title', query)).filter(similarity__gt=0.1)
            results2=Post.published.annotate(similarity=TrigramSimilarity('description', query)).filter(similarity__gt=0.1)
            imagetitles=Post.published.annotate(similarity=TrigramSimilarity('images__title', query)).filter(similarity__gt=0.1)
            imagediscription=Post.published.annotate(similarity=TrigramSimilarity('images__description', query)).filter(similarity__gt=0.1)
            results=(results1|results2|imagetitles|imagediscription)
            # 

    context={
        'query':query,
        'results':results,
    }
    return render(request,'blog/search.html',context)

@login_required
def craete_post(request):
    if request.method == 'POST':
        form = CraetePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post = post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post = post)
            return redirect('blog:profile')
    else:
        form = CraetePostForm()
    return render(request, 'forms/craete_post.html', {'form':form})

@login_required
def profile(request):
    user=request.user
    posts=Post.published.filter(author=user)
    comments=Comment.objects.filter(post__author=user).filter(active=True)

    # pagination for posts
    paginator1 = Paginator(posts, 10)
    posts_list = paginator1.get_page(request.GET.get('page'))
    
    # paginstion for comments
    paginator2 = Paginator(comments, 10)
    comment_list = paginator2.get_page(request.GET.get('page2'))

    context={
        'posts_list':posts_list,
        'comment_list':comment_list,
    }        
    return render(request,"blog/profile.html" ,context)

@login_required
def delete_post(request, post_id):
    post=get_object_or_404(Post , id=post_id)
    if request.method=='POST':
        post.delete()
        return redirect("blog:profile")
    return render(request,"forms/delete_post.html", {'post':post})

@login_required
def delete_image(request, image_id):
    image= get_object_or_404(Image, id=image_id)
    image.delete()
    return redirect('blog:profile')

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post , id=post_id)
    if request.method == 'POST':
        form = CraetePostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post = post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post = post)
            return redirect('blog:edit_post')
    else:
        form = CraetePostForm(instance=post)
    return render(request, 'forms/craete_post.html', {'form':form,'post':post})


class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:index')
        return render(request, self.template_name, {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user':user})
    else:
        form=UserRegisterForm()
    return render(request, 'registration/register.html', {'form':form})


@login_required
def edit_account(request):
    if request.method == 'POST':
        user_form=UserEditForm(request.POST, instance=request.user)
        account_form=AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form=UserEditForm(instance=request.user)
        account_form=AccountEditForm(instance=request.user.account)
    context={
        'user_form':user_form,
        'account_form':account_form
    }
    return render(request, 'registration/edit_account.html',context)

def author_info(request, author_id):
    posts= Post.published.all().filter(author__id=author_id)
    user=User.objects.get(id=author_id)
    mp= Post.published.all().filter(author__id=author_id).annotate(comments_count=Count('comments')).order_by('-comments_count').last

    context={
        'user':user,
        'posts':posts,
        'mp':mp
    }
    return render(request, 'blog/author_info.html', context)