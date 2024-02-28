from django.contrib import admin
from .models import *
# Register your models here.


# admin.site.register(post)
@admin.register(post) 

class PostAdmin(admin.ModelAdmin):
    list_display = [ 'author' , 'title' , 'publish' , 'Status']
    ordering = ['title' , 'publish']
    list_filter = ['Status', 'publish', 'author']    
    search_fields = ['title', 'content']
    raw_id_fields = ['author'] 
    date_hierarchy = 'publish'   # Allows for filtering by date in the admin interface
    prepopulated_fields = {'slug':['title']}
    # list_editable = ['status'] (bug)
    list_display_links = ['author']