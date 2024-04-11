from django.shortcuts import render,get_list_or_404 ,redirect , get_object_or_404
from django.http import HttpResponse,Http404
from .models import *
from .froms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#for class based views
from django.views.generic import ListView,DeleteView
import datetime
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    return HttpResponse("index")
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
    post = get_list_or_404(request , id=post_id , status=Post.Status.PUBLISHED)
    comment=None
    form=Commentform(data=request.Post)
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