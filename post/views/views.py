from django.http import Http404
from rest_framework import status, exceptions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post, Comment
from post.serializers import PostShortSerializer, PostFullSerializer, CommentSerializer, PostFullSerializer2
from utils.permissions import IsOwnerOrReadOnly


class PostListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        print(request.query_params)
        projects = Post.objects.all()
        serializer = PostShortSerializer(projects, many=True)
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

    def get_object(self, pk, request):
        try:
            post = Post.objects.get(id=pk)
            if not self.check_object_permissions(request, post):
                raise exceptions.PermissionDenied(detail="You don't have permission.")
            return post
        except Post.DoesNotExist:
            raise Http404

    def check_object_permissions(self, request, obj):
        if request.method in ['GET']:
            return True

        return obj.creator == request.user

    def get(self, request, pk):
        post = self.get_object(pk, request)
        serializer = PostFullSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk, request)
        serializer = PostFullSerializer2(instance=post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        post = self.get_object(pk, request)
        post.delete()
        return Response('Post with ID: {} was deleted.'.format(pk), status=status.HTTP_204_NO_CONTENT)


class CommentListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_object(self, pk, request):
        try:
            post = Post.objects.get(id=pk)
            if not self.check_object_permissions(request, post):
                raise exceptions.PermissionDenied(detail="You don't have permission.")
            return post
        except Post.DoesNotExist:
            raise Http404

    def check_object_permissions(self, request, obj):
        if request.method in ['GET']:
            return True

        return obj.creator == request.user

    def get(self, request, pk):
        post = self.get_object(pk, request)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        post = self.get_object(pk, request)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentDetailAPIView(APIView):
    http_method_names = ['put', 'delete']
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def get_object(self, pk, request):
        try:
            comment = Comment.objects.get(id=pk)
            if not self.check_object_permissions(request, comment):
                raise exceptions.PermissionDenied(detail="You don't have permission.")
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def check_object_permissions(self, request, obj):
        if request.method in ['GET']:
            return True

        return obj.creator == request.user

    def put(self, request, pk):
        comment = self.get_object(pk, request)
        serializer = CommentSerializer(instance=comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        comment = self.get_object(pk, request)
        comment.delete()
        return Response('Deleted comment with ID: {}'.format(pk), status=status.HTTP_204_NO_CONTENT)
