from django.contrib import admin
from .models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # fields = ('title','slug', 'author', 'publish', 'status')
    list_display = ('title', 'author', 'slug', 'text', 'created', 'updated', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('slug', 'title', 'text')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('status', 'publish')
    date_hierarchy = 'publish'
    row_id_fields = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'text', 'created_at', 'updated_at', 'active')
    list_filter = ('active', 'updated_at', 'created_at')
    search_fields = ('name', 'email', 'text')
