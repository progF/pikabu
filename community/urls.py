from django.urls import path
from community.views import CommunityAPIView, CommunityDetailAPIView, subscription_view, community_posts
from rest_framework import routers

urlpatterns = [
    path('communities/', CommunityAPIView.as_view()),
    path('communities/<int:pk>/', CommunityDetailAPIView.as_view()),
    path('communities/<int:pk>/posts', community_posts),
    path('subscribe_to/<int:pk>/', subscription_view)
]

router = routers.DefaultRouter()
urlpatterns += router.urls
