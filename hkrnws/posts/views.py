from hkrnws.accounts import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from hkrnws.posts.models import CrawlRun, Post
from hkrnws.posts.serializers import PostActionRequest, PostsResponseSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def posts_list(request):
    try:
        request_token = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
        user = Token.objects.get(pk=request_token).user
        last_crawl_instance = CrawlRun.objects.latest('created_at')
        latest_posts = Post.objects.filter(crawl_run=last_crawl_instance)
        serializer = PostsResponseSerializer(list(latest_posts), many=True)
        return Response(serializer.data)

    except Exception as e:
        raise APIException(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post(request):
    try:
        unsafe_request_data = request.data
        request_token = request.META['HTTP_AUTHORIZATION'].split(' ')[-1]
        user = Token.objects.get(pk=request_token).user

        serializer = PostActionRequest(data=unsafe_request_data)
        if serializer.is_valid(raise_exception=True):
            request_data = serializer.validated_data
            post = Post.objects.get(pk=request_data['id'])
            
            if(request_data['action'] == 'hide'):
                post.deleted_by.add(user)
            else:
                post.read_by.add(user)

            return Response({'details': 'success'}, status=200)

    except ValueError as e:
        raise APIException(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)
