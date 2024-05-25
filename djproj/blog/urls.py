#created by myself
from django.urls import URLPattern, path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = "blog"

urlpatterns=[
    
    path('',views.index, name='index'),

    path('posts/',views.post_list,name='post_list'),
    path('posts/<str:category>',views.post_list,name='post_list_category'),   
    
     # path('posts/',views.PostListView.as_view(),name='post_list'),

    path('posts/detail/<int:id>',views.post_detail,name='post_detail'), 

    # path('posts/<pk>',views.PostDetailView.as_view(),name='post_detail'),

    path('posts/<post_id>/comment',views.post_comment,name='post_comment'),

    path('ticket/',views.ticket,name="ticket"),

    path('search/',views.post_search ,name="post_search"),

    path('profile/',views.profile ,name="profile"),

    path('profile/craete_post/',views.craete_post,name='craete_post'),

    path('profile/craete_post/<post_id>',views.edit_post,name='edit_post'),

    path('profile/delete_post/<post_id>', views.delete_post, name='delete_post'),

    path('profile/delete_image/<image_id>', views.delete_image, name='delete_image'),

    path('login/', views.LoginView.as_view(), name='login'), 
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url='/password-reset/complete'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('register', views.register, name='register'),

    path('account/edit', views.edit_account, name='edit_account'),

    path('author_info/<int:author_id>', views.author_info, name='author_info'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
