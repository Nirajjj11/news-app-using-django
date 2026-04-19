from django.urls import path
from .views import (
      ArticleListView,
      ArticleDeleteView,
      ArticleDetailView,
      ArticleUpdateView,
)

urlpatterns =[
      path("",ArticleListView.as_view(), name="article_list"),
      path("<int:pk>/",ArticleDetailView.as_view(), name="articles_details"),
      path("<int:pk>/delete",ArticleDeleteView.as_view(), name="article_delete"),
      path("<int:pk>/edit/", ArticleUpdateView.as_view(), name="article_edit")
]