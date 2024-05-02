from django.contrib import admin
from .models import *
# Register your models here.

admin.sites.AdminSite.site_header = "پنل مدیریت"
admin.sites.AdminSite.site_title = "پنل "
admin.sites.AdminSite.index_title = "دسترسی ها"

#inline
class CommentInline(admin.TabularInline):
    model=Comment
    extra=0
class ImageInline(admin.StackedInline):
    model=Image
    extra=0


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

    inlines=[ImageInline, CommentInline]

@admin.register(Ticket) 
class TicketAdmin(admin.ModelAdmin):
    list_display=('name','subject','phone')

@admin.register(Comment) 
class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'post' , 'name' , 'created' , 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'body']
    list_editable = ['active'] 

@admin.register(Image) 
class ImageAdmin(admin.ModelAdmin):
     list_display = [ 'post' , 'title' , 'created']