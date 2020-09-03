from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view
from account.api.serializers import RegistrationSerializer
from account.api.serializers import AccountSerializer
from account.models import Account
from account.api.serializers import UsernameInfoSerializer
from account.api.serializers import EmailInfoSerializer
from account.api.serializers import PasswordInfoSerializer
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
            try:
                account = serializer.save()
                data['username'] = account.username
                token = Token.objects.get(user=account).key
                data['token'] = token
            except :
                data['detail'] = serializer.errors
        else:
            if serializer.errors.get('email') is not None:
                data['detail_email'] = serializer.errors.get('email')[0].capitalize()
            if serializer.errors.get('username') is not None:
                data['detail_username'] = serializer.errors.get('username')[0].capitalize()
        return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_username(request):
    serializer = UsernameInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        user.username = profile_info.username
        try:
            user.save()
            data['username'] = user.username
            data['detail'] = 'Username changed to: ' + user.username
        except :
            data['detail'] = 'User with that username already exists'
    else:
        data['detail'] = serializer.errors
    return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_email(request):
    serializer = EmailInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        user.email = profile_info.email
        try:
            user.save()
            data['email'] = user.email
            data['detail'] = 'Email changed to: ' + user.email
        except :
            data['detail'] = 'User with that email already exists'
    else:
        data['detail'] = serializer.errors
    return Response(data)

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_password(request):
    serializer = PasswordInfoSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        profile_info = serializer.save()
        user = request.user
        if user.check_password(profile_info.password):
            user.set_password(profile_info.new_password)
            user.save()
            data['detail'] = 'Password changed'
        else:
            data['detail'] = 'Wrong password'
    else:
        data['detail'] = serializer.errors
    return Response(data)


@api_view(['GET',])
@authentication_classes([])
@permission_classes([])
def get_logo(request):
    img = open('media/logo/logo.png', 'rb')
    response = FileResponse(img)
    return response