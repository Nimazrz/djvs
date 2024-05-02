#created by myself
from django.urls import URLPattern, path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "blog"

urlpatterns=[
    
    path('',views.index, name='index'),
    # path('posts/',views.post_list,name='post_list'),  #this changes is for class based views
    path('posts/',views.PostListView.as_view(),name='post_list'),

    path('posts/write/',views.post_write,name='post_write'),
     
    path('posts/<int:id>',views.post_detail,name='post_detail'), # this changes is for class based views

    # path('posts/<pk>',views.PostDetailView.as_view(),name='post_detail'),

    path('posts/<post_id>/comment',views.post_comment,name='post_comment'),

    path('ticket/',views.ticket,name="ticket"),

    path('search/',views.post_search ,name="post_search"),

    path('profile/',views.profile ,name="profile"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)