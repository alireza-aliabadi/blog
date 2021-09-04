from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page = request.GET.get('page-num')
    pages_range_str = '['
    try:
        posts = paginator.page(page)
        pages_range = paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
    except PageNotAnInteger:
        posts = paginator.page(1)
        pages_range = paginator.get_elided_page_range(1, on_each_side=1, on_ends=1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        pages_range = paginator.get_elided_page_range(paginator.num_pages, on_each_side=1, on_ends=1)
    for item in pages_range:
        pages_range_str += str(item)
    return render(request, 'blog/posts/list.html', {'posts': posts, 'pages_range': pages_range_str + ']',
                                                    'tag': tag})


class PostListView(ListView):
    queryset = Post.published.all()
    page_kwarg = 'page-num'
    paginate_by = 3
    context_object_name = 'posts'
    template_name = 'blog/posts/list.html'


def post_detail(request, year, month, day, post_slug):
    post = get_object_or_404(Post, slug=post_slug, status='published',
                             publish__year=year, publish__month=month, publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tag=Count('tags')).order_by('-same_tag', '-publish')[:4]
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    return render(request, 'blog/posts/detail.html', {'detail': post, 'comments': comments,
                                                      'comment_form': comment_form, 'new_comment': new_comment,
                                                      'similar_posts': similar_posts})


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    form = EmailPostForm()
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends you read {post.title}"
            message = f"read {post.title} at {post_url} \n\n {data['name']} comments: {data['comment']}"
            send_mail(subject, message, "alirezara98@gmail.com", [data['to'], ])
            sent = True
    return render(request, 'blog/posts/share.html', {'post': post, 'form': form, 'sent': sent})
