from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from tag.models import Tag
from tag.serializers import (
    TagSerializer
)
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
import logging

logger = logging.getLogger(__name__)


class TagViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tag_subscription(request, pk):
    tag = get_object_or_404(Tag, id=pk)
    if request.user in tag.subscribed_users.all():
        tag.subscribed_users.remove(request.user)
        logger.info('user with id: {} unsubscribed from tag: #{}'.format(request.user.id, tag.name))
        return Response("Unsubscribed from #{}".format(tag.name))
    else:
        tag.subscribed_users.add(request.user)
        logger.info('user with id: {} subscribed to tag: #{}'.format(request.user.id, tag.name))
        return Response("Subscribed to #{}".format(tag.name))
