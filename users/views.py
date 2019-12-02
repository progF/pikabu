from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from users.models import Profile, UserRelation, MainUser
from users.serializers import (
    MainUserSerializer,
    ProfileSerializer,
    ProfileShortSerializer
)
from rest_framework import viewsets
from rest_framework import mixins
from users.permissions import UserPermissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MainUserSerializer


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    # serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions,)

    def get_serializer_class(self):
        serializer_class = None
        if self.action == 'list':
            serializer_class = ProfileShortSerializer
        else:
            serializer_class = ProfileSerializer
        return serializer_class


class UserViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = MainUserSerializer

    def get_object(self):
        return self.request.user


@api_view(['POST'])
def subscription_view(request, pk):
    subscribed_to = get_object_or_404(MainUser, id=pk)
    try:
        relation = UserRelation.objects.get(Q(subscriber=request.user) & Q(subscribed_to=subscribed_to))
        relation.delete()
        return Response("Unsubscribed!")
    except Exception:
        relation = UserRelation.objects.create(subscriber=request.user,subscribed_to=subscribed_to)
        return Response("Now you subscribed to {}".format(relation.subscribed_to.username))
