from django.urls import path
# from rest_framework_jwt.views import obtain_jwt_token
from users.views import RegisterViewSet, ProfileViewSet, UserViewSet
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('profile/', ProfileViewSet.as_view({
        'get':'retrieve',
        'put':'update'}), name='profile-detail'),

    path('delete/', UserViewSet.as_view({
        'delete':'destroy'}), name='delete-user'),
]
router = routers.DefaultRouter()
router.register('register', RegisterViewSet, base_name='users')
urlpatterns += router.urls