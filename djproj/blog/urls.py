#created by myself
from django.urls import URLPattern, path
from . import views

app_name = "blog"

urlpatterns=[
    
    path('',views.index, name='index'),
    path('posts/',views.post_list,name='post_list'),
    path('posts/<int:id>',views.post_detail,name='post_detail')
    
]