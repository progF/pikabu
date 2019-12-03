from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from post.models import Post
from post.serializers import PostFullSerializer, CommentSerializer
from tag.models import PostTagMap
from users.models import Profile, UserRelation, MainUser
from users.serializers import (
    MainUserSerializer,
    ProfileSerializer,
    ProfileShortSerializer
)
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count

from utils.constants import BY_TIME_ASC
from utils.permissions import UserPermissions
import logging

logger = logging.getLogger(__name__)

class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = MainUserSerializer


class ProfileViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly, UserPermissions, )
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ProfileShortSerializer
        return ProfileSerializer


class UserViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = MainUserSerializer

    def get_object(self):
        return self.request.user


class UserInfoViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )

    @action(methods=['GET'], detail=False, url_path='newsfeed/subscriptions', url_name='newsfeed/subscriptions')
    def newsfeed_subscriptions(self, request):
        posts = Post.objects.filter(creator__my_subscribers__subscriber_id=self.request.user.id)
        posts = posts.annotate(rating=Count('ratings')).filter(rating__gte=request.user.profile.post_rating)
        serializer = PostFullSerializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='newsfeed/communities', url_name='newsfeed/communities')
    def newsfeed_communities(self, request):
        posts = Post.objects.filter(community__my_users__user_id=self.request.user.id)
        posts = posts.annotate(rating=Count('ratings')).filter(rating__gte=request.user.profile.post_rating)
        serializer = PostFullSerializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='newsfeed/tags', url_name='newsfeed/tags')
    def newsfeed_tags(self, request):
        tags = request.user.subscribed_tags.all()
        post_tag_map = PostTagMap.objects.filter(tag_id__in=tags.values_list('id'))
        posts = Post.objects.filter(id__in=post_tag_map.values_list('post_id'))
        posts = posts.annotate(rating=Count('ratings')).filter(rating__gte=request.user.profile.post_rating)
        serializer = PostFullSerializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def saved_posts(self, request):
        saved = request.user.saved_posts.all()
        posts = Post.objects.filter(id__in=saved.values_list('post_id'))
        serializer = PostFullSerializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def posts(self, request):
        posts = request.user.posts
        serializer = PostFullSerializer(posts, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def comments(self, request):
        order_by = request.user.profile.comment_sorting
        if order_by == BY_TIME_ASC:
            comments = request.user.comments.all().order_by('created_at')
        else:
            comments = request.user.comments.all().order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def subscription_view(request, pk):
    subscribed_to = get_object_or_404(MainUser, id=pk)

    try:
        relation = UserRelation.objects.get(Q(subscriber=request.user) & Q(subscribed_to=subscribed_to))
        relation.delete()
        logger.info('user with id: {} unsubscribed from user with id: {}'.format(request.user.id, pk))
        return Response("Unsubscribed from {}.".format(relation.subscribed_to.username))
    except Exception:
        relation = UserRelation.objects.create(subscriber=request.user, subscribed_to=subscribed_to)
        logger.info('user with id: {} subscribed to user with id: {}'.format(request.user.id, pk))
        return Response("You subscribed to {}.".format(relation.subscribed_to.username))
