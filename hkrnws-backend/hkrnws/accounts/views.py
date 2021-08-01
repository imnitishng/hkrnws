from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated 

from hkrnws.accounts.serializers import UserRegistrationSerializer


@api_view(['POST'])
def user_registration(request):
    try:
        response = {}
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.save()
            response["email"] = account.email
            response["username"] = account.username
            response["message"] = "User registered successfully"
            return Response(response, status=status.HTTP_201_CREATED)

        else:
            response = serializer.errors
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    except ValueError as e:
        raise APIException(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)
