from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from post.models import Post, PostRating


@api_view(['POST'])
def post_rating(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404

    try:
        rating = PostRating.objects.get(post=post, user=request.user)
        rating.delete()
    except PostRating.DoesNotExist:
        PostRating.objects.create(user=request.user, post=post)

    return Response("OK", status=status.HTTP_202_ACCEPTED)
