from django.urls import path
from .views import post_list, post_detail, PostListView, post_share
from .feeds import PostFeed

app_name = 'post'
urlpatterns = [
    path('', post_list, name='post-list'),
    path('tag/<slug:tag_slug>', post_list, name="post-list-by-tag"),
    # path('', PostListView.as_view(), name="post-list"),
    path('post-detail/<int:year>-<int:month>-<int:day>/<slug:post_slug>', post_detail, name='post-detail'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('feed/', PostFeed(), name='post_feed')
]
