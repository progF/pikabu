from django.db.models import F, Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from post.models import Post, PostRating, SavedPost
from users.models import Profile


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def post_rating(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = Profile.objects.filter(id=request.user.id)

    try:
        rating = PostRating.objects.get(Q(post=post) & Q(user=request.user))
        rating.delete()
        user.update(rating=F('rating') - 1)
    except PostRating.DoesNotExist:
        PostRating.objects.create(user=request.user, post=post)
        user.update(rating=F('rating') + 1)

    return Response("OK", status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def save_post(request, pk):
    post = Post.objects.get(id=pk)
    try:
        saved_post = SavedPost.objects.get(Q(post=post) & Q(user=request.user))
        saved_post.delete()
        return Response('Deleted post with ID: {} from bookmarks.'.format(post.id),
                        status=status.HTTP_204_NO_CONTENT)
    except SavedPost.DoesNotExist:
        SavedPost.objects.create(user=request.user, post=post)
        return Response('Saved post with ID: {} in bookmarks.'.format(post.id), status=status.HTTP_201_CREATED)