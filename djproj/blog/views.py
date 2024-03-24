from django.shortcuts import render,get_list_or_404 ,redirect
from django.http import HttpResponse,Http404
from .models import *
from .froms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
#for class based views
from django.views.generic import ListView,DeleteView
import datetime
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

#>> ________________________________________________________________________________________________________________
# def post_detail(request,id):
#     try:
#         post=Post.published.get(pk=id) # get the object with this id or raise an
#     except:
#         raise Http404("NO POST FOUND")
    
#     context={
#         'post':post,
#         'new_date' :datetime.datetime.now()
        
#         }

#     return render(request,"blog/detail.html",context)
# ________________________________________________________________________________________________________________

class PostDetailView(DeleteView):
    model=Post
    template_name='blog/detail.html'


def ticket(request):
    if request.method == "POST":
        
        form =TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect('blog:index')
    
    else:
        form = TicketForm()
    return render(request,"forms/ticket.html" , {'form':form})