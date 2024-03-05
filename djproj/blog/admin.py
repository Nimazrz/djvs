from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(post)
@admin.register(Post) 

class PostAdmin(admin.ModelAdmin):
    list_display = [ 'title' , 'author' , 'publish' , 'status']
    ordering = ['title' , 'publish'] #sort
    list_filter = ['status', 'publish', 'author']    
    search_fields = ['title', 'content']
    raw_id_fields = ['author'] 
    date_hierarchy = 'publish'   # Allows for filtering by date in the admin interface
    prepopulated_fields = {'slug':['title']}
    list_editable = ['status'] 
    list_display_links = ['title']