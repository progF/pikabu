from django.shortcuts import render
from community.serializers import CommunityShortSerializer, CommunitySerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from community.models import Community,CommunityMember
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from django.db.models import Q


class CommunityAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request):
        communities = Community.objects.all()
        serializer = CommunityShortSerializer(communities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CommunityShortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


class CommunityDetailAPIView(APIView):
    http_method_names = ['get', 'put', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self, pk):
        try:
            return Community.objects.get(pk=pk)
        except Community.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        community = self.get_object(pk)
        serializer = CommunitySerializer(community)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        community = self.get_object(pk)
        serializer = CommunitySerializer(community, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        community = self.get_object(pk)
        community.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def subscription_view(request, pk):
    subscribed_to = get_object_or_404(Community, id=pk)
    try:
        membership = CommunityMember.objects.get(Q(user=request.user) & Q(community=subscribed_to))
        membership.delete()
        return Response("Unsubscribed!")
    except Exception:
        relation = CommunityMember.objects.create(user=request.user,community=subscribed_to)
        return Response("Now you subscribed to {}".format(relation.community.name))
