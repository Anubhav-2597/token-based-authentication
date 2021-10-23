from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import ListUserModel
from accounts.serializers import UserListSerializer


class ListUsers(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        username = [user.username for user in User.objects.all()]
        return Response(username)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        try:
            user_token = Token.objects.get(user=user)
            user_token.delete()
        except Token.DoesNotExist:
            pass
        finally:
            user_token = Token.objects.create(user=user)

        return Response({
            'token': user_token.key,
            'user_id': user.pk,
            'email': user.email
        })


class ListUserAPIView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
            Get method to get list of users
        """

        get_users = ListUserModel.objects.all()

        if not get_users:
            return Response("no users existing")

        user_list_serializer = UserListSerializer(get_users, many=True)

        return Response({"users": user_list_serializer.data})

    def post(self, request):
        """
        Post method to add new user in db
        """

        request_body_params = request.data.copy()

        user_serializer = UserListSerializer(data=request_body_params)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors)

        user_serializer.save()

        return Response(data=user_serializer.data)
