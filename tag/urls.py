from django.urls import path
from rest_framework import routers
from tag.views import TagViewSet, tag_subscription

urlpatterns = [
    path('subscribe_to_tag/<slug:name>/', tag_subscription)
]

router = routers.DefaultRouter()
router.register('tag',TagViewSet, base_name='tag')
urlpatterns += router.urls
