from django.urls import path
from rest_framework import routers

urlpatterns = [
    # path('posts/'),
    # path('posts/<int:pk>'),
    # path('posts/<int:pk>/comments'),
]

router = routers.DefaultRouter()
# router.register('register', RegisterViewSet, base_name='users')
urlpatterns += router.urls
