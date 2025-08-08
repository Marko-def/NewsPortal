from django.urls import path
from .views import (news_list, news_detail,
    NewsCreate,
    ArticleCreate,
    NewsUpdate,
    ArticleUpdate,
    NewsDelete,
    ArticleDelete,
    PostCreateView, PostUpdateView
)
urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('<int:id>/', news_detail, name='news_detail'),
    path('news/search/', news_list, name='news_search'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),

    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
]