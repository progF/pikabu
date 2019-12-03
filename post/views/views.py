from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, Comment
from post.serializers import PostShortSerializer, PostFullSerializer, PostFullSerializer2, \
    CommentWithCreatorSerializer
from utils.permissions import IsOwnerOrReadOnly
import logging

logger = logging.getLogger(__name__)


class PostListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        params = request.query_params
        date = params.get('date')
        sort = params.get('sort')
        if date:
            posts = Post.posts.get_posts_by_date(date)
        elif sort:
            posts = Post.posts.sort_by_field(sort)
        else:
            posts = Post.objects.all()

        serializer = PostShortSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostFullSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PostDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get_object(self, pk):
        return get_object_or_404(Post, id=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = PostFullSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostFullSerializer2(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        post = self.get_object(pk)
        post.delete()
        logger.info('post with id: {} deleted.'.format(pk))
        return Response('Post with ID: {} was deleted.'.format(pk), status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, pk):
        return get_object_or_404(Post, id=pk)

    def get(self, request, pk):
        post = self.get_object(pk)
        comments = post.comments.all()
        serializer = CommentWithCreatorSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = self.get_object(pk)
        serializer = CommentWithCreatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailAPIView(APIView):
    http_method_names = ['put', 'delete']
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk):
        return get_object_or_404(Comment, id=pk)

    def put(self, request, pk):
        comment = self.get_object(pk)
        serializer = CommentWithCreatorSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        comment = self.get_object(pk)
        comment.delete()
        logger.info('comment with id: {} deleted'.format(pk))
        return Response('Deleted comment with ID: {}'.format(pk), status=status.HTTP_204_NO_CONTENT)
