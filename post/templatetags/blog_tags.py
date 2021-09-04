from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown

register = template.Library()


@register.simple_tag
def total_posts_tag():
    return Post.published.count()


@register.inclusion_tag('blog/side_menu/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    context = {'latest_posts': latest_posts}
    return context


@register.simple_tag(name="most_commented_posts")
def show_most_commented(count=5):
    posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    return posts


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='fa_plural')
def persian_plural(number):
    if number > 1:
        return mark_safe('<span>ها</span>')
    return mark_safe('<span></span>')
