from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import ListItemModel
from accounts.serializers import ItemSerializer


class ListItems(APIView):
    """
    View to list all Items in the system.

    * Requires token authentication.
    * Only admin Items are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all Items.
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


class ListItemAPIView(APIView):

    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
            Get method to get list of Items
        """

        get_Items = ListItemModel.objects.all()

        if not get_Items:
            return Response({"Items": []})

        user_list_serializer = ItemSerializer(get_Items, many=True)

        return Response({"Items": user_list_serializer.data})

    def post(self, request):
        """
        Post method to add new user in db
        """

        request_body_params = request.data.copy()

        user_serializer = ItemSerializer(data=request_body_params)

        if not user_serializer.is_valid():
            return Response(user_serializer.errors)

        user_serializer.save()

        return Response(data=user_serializer.data)
