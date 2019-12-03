from django.urls import path
from rest_framework import routers
from tag.views import TagViewSet, tag_subscription

urlpatterns = [
    path('tags/<int:pk>/subscribe', tag_subscription)
]

router = routers.DefaultRouter()
router.register('tags', TagViewSet, base_name='tags')
urlpatterns += router.urls
