from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.template.defaultfilters import truncatewords
from .models import Post


class PostFeed(Feed):
    title = 'my blog'
    link = reverse_lazy('post:post-list')
    description = 'my blog feed'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.text, 30)
