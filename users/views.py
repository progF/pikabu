from django.shortcuts import render
from rest_framework.viewsets import mixins, GenericViewSet
from users.serializers import MainUserSerializer, ProfileSerializer


class RegisterViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = MainUserSerializer

class ProfileViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
