from rest_framework.permissions import IsAuthenticated

from users.serializers import MainUserSerializer, ProfileSerializer
from rest_framework import viewsets
from rest_framework import mixins


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MainUserSerializer


class ProfileViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class UserViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MainUserSerializer

    def get_object(self):
        return self.request.user
