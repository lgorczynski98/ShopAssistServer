from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from account.api.serializers import RegistrationSerializer
from account.api.serializers import AccountSerializer
from account.models import Account
from account.api.serializers import ProfilesInfoSerializer
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

class AccountList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountDetail(generics.RetrieveUpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
        })


@api_view(['POST',])
@authentication_classes([])
@permission_classes([])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_username(request):
    serializer = ProfilesInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        user.username = profile_info.username
        user.save()
        data['username'] = user.username
        data['detail'] = 'Username changed to: ' + user.username
    else:
        data['detail'] = serializer.errors
    return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_email(request):
    serializer = ProfilesInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        user.email = profile_info.email
        user.save()
        data['email'] = user.email
        data['detail'] = 'Email changed to: ' + user.email
    else:
        data['detail'] = serializer.errors
    return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_password(request):
    serializer = ProfilesInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        user.set_password(profile_info.password)
        user.save()
        data['detail'] = 'Password changed'
    else:
        data['detail'] = serializer.errors
    return Response(data)