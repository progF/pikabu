from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from post.models import Post, PostRating
from users.models import Profile


@api_view(['POST'])
def post_rating(request, pk):
    post = get_object_or_404(Post, id=pk)
    user = Profile.objects.filter(id=request.user.id)

    try:
        rating = PostRating.objects.get(post=post, user=request.user)
        rating.delete()
        user.update(rating=F('rating') - 1)
    except PostRating.DoesNotExist:
        PostRating.objects.create(user=request.user, post=post)
        user.update(rating=F('rating') + 1)

    return Response("OK", status=status.HTTP_202_ACCEPTED)
