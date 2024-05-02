from django.shortcuts import render,get_list_or_404 ,redirect , get_object_or_404
from django.http import HttpResponse,Http404
from django.contrib.auth.decorators import login_required
from .models import *
from .froms import *
from .froms import PostForm
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#for class based views
from django.views.generic import ListView,DeleteView
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery ,SearchRank, TrigramSimilarity
# Create your views here.

def index(request):
    return render(request , "blog/index.html" )
#>> ______________________________________________________________________________________________________________________________________
# def post_list(request):

#     posts = Post.published.all()

#     paginator = Paginator(posts, 2) #
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         raise Http404("Sorry! That page does not exist.")# posts = paginator.page(paginator.num_pages) <we can use this insted that>
#     except PageNotAnInteger:
#         posts = paginator.page(1)
        
#     context={
#         'posts':posts
#         }
#     return render(request,'blog/list.html',context)
# _______________________________________________________________________________________________________________________________________

# its for class based views
class PostListView(ListView):
    # model=Post
    queryset=Post.published.all()
    context_object_name='posts'
    paginate_by=3
    template_name='blog/list.html'

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


@login_required
def post_write(request):
    if request.method == 'POST':
        print(f'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa :  {PostForm.clean_writer}')
        title = request.POST['title']
        description = request.POST['description']
        readingtime = request.POST['readingtime']
        slug = PostForm.slugy(request.POST['title'])
        author = request.user
        post = Post.objects.create(title=title, description=description, author=author, readingtime=readingtime,slug=slug)
        return redirect('blog:index')
    return render(request, 'forms/write.html')

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

def profile(request):
    user=request.user
    posts=Post.published.filter(author=user)
    return render(request,"blog/profile.html" ,{'posts':posts})
   