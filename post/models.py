from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    status_choices = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]
    author = models.ForeignKey(User, on_delete=CASCADE, related_name="blog_posts",
                               related_query_name="blog_posts")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique_for_date="publish", db_index=True, allow_unicode=True)
    text = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=status_choices, default='draft')
    tags = TaggableManager()

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    objects = models.Manager()
    published = PostManager()

    def get_absolute_url(self):
        return reverse('post:post-detail',
                       args=[self.publish.year, self.publish.month, self.publish.day, self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name="comments", related_query_name="comments")
    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created_at',)

    def __Str__(self):
        return f'Comment by {self.name} on {self.post}'
