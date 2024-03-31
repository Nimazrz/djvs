#created by myself
from django.urls import URLPattern, path
from . import views

app_name = "blog"

urlpatterns=[
    
    path('',views.index, name='index'),
    # path('posts/',views.post_list,name='post_list'),  #this changes is for class based views
    path('posts/',views.PostListView.as_view(),name='post_list'),
    # path('posts/<int:id>',views.post_detail,name='post_detail') # this changes is for class based views
    path('posts/<pk>',views.PostDetailView.as_view(),name='post_detail'),

    path('ticket/',views.ticket,name="ticket"), # this is fot forms
    
]