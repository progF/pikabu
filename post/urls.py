from django.urls import path

from post.views import *

urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('posts/<int:pk>', PostDetailAPIView.as_view()),
    path('posts/<int:pk>/rating', post_rating),
    path('posts/<int:pk>/comments', CommentListAPIView.as_view()),
    path('comments/<int:pk>', CommentDetailAPIView.as_view()),
    path('posts/<int:pk>/save', save_post)
]
