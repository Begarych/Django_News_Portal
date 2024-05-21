from django.urls import path
from .views import (
   PostList, PostDetail, SearchList, CreateNews, PostEdit, NewsEdit, PostDelete, NewsDelete, subscriptions
)


urlpatterns = [
   path('', PostList.as_view(), name="post_list"),
   path('search/', SearchList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name="post_detail"),
   path('create/news/', CreateNews.as_view(), name="news_create"),
   path('create/post/', CreateNews.as_view(), name="post_create"),
   path('post/<int:pk>/edit/', PostEdit.as_view(), name='post_update'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_update'),
   path('post/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('subscriptions/', subscriptions, name='subscriptions'),
]
