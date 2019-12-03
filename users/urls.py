from django.urls import path
from users.views import RegisterViewSet, ProfileViewSet, UserViewSet, subscription_view, UserInfoViewSet
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('delete/', UserViewSet.as_view({'delete': 'destroy'}), name='delete-user'),
    path('subscribe_to/<int:pk>/', subscription_view)
]

router = routers.DefaultRouter()
router.register('info', UserInfoViewSet, base_name='users')
router.register('register', RegisterViewSet, base_name='users')
router.register('profile', ProfileViewSet, base_name='users')
urlpatterns += router.urls
