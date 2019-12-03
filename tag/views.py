from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from tag.models import Tag, PostTagMap
from tag.serializers import (
    TagSerializer
)
from rest_framework import viewsets
from rest_framework import mixins
from users.permissions import UserPermissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q


class TagViewSet(mixins.CreateModelMixin,mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tag_subscription(request, name):
    tag = get_object_or_404(Tag, name=name)
    if request.user in tag.subscribed_users.all():
        tag.subscribed_users.remove(request.user)
        return Response("Unsubscribed!")
    else:
        tag.subscribed_users.add(request.user)
        return Response("Now you subscribed to {}".format(tag.name))
