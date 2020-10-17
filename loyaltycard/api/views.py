from loyaltycard.models import Loyaltycard
from account.models import Account
from loyaltycard.api.serializers import LoyaltycardSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view
import os
from django.core.files.base import ContentFile
from pyfcm import FCMNotification
import string
import random
from datetime import datetime

FIREBASE_API_KEY = 'AAAAPkSbPLg:APA91bENvZODi1GwJkXOj886CRkr2EkIS9g1seuJ2hDQnkll5cFpe7seLQdjPTX6sjm_5xjIIz7QGSYtGptZSoiz4K2dSX6cv47wyfJugryjmWBAtoT9DU4edOs1qla2NYzmJjbm0pXP'

@permission_classes((IsAuthenticated,))
class LoyaltycardList(generics.ListCreateAPIView):
    queryset = Loyaltycard.objects.all()
    serializer_class = LoyaltycardSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = Loyaltycard.objects.filter(owner=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

@permission_classes((IsAuthenticated,))
class LoyaltycardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loyaltycard.objects.all()
    serializer_class = LoyaltycardSerializer
    
    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            if instance.image.name != 'loyaltycards/default.jpg':
                os.remove(instance.image.path)
            instance.delete()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.owner == self.request.user:
            serializer.save()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == request.user:
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)
        data = {}
        data['detail'] = "You don't have permission"
        return Response(data, status=403)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == self.request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        data = {}
        data['detail'] = "You don't have permission"
        return Response(data, status=403)


@permission_classes((IsAuthenticated,))
@api_view(['GET',])
def get_loyaltycard_image(request, loyaltycard_id):
    loyaltycard = Loyaltycard.objects.get(id=loyaltycard_id)
    if loyaltycard.owner == request.user:
        img = open(loyaltycard.image.path, 'rb')
        response = FileResponse(img)
        return response
    data = {}
    data['detail'] = "You don't have permission"
    return Response(data, status=403)

@permission_classes((IsAuthenticated,))
@api_view(['POST',])
def share_loyalty_card(request, loyaltycard_id, username):
    loyaltycard = Loyaltycard.objects.get(id=loyaltycard_id)
    data = {}
    if loyaltycard.owner == request.user:
        try:
            user_to_share = Account.objects.get(username=username)
            loyaltycard.pk = None
            if loyaltycard.image.name != 'loyaltycards/default.jpg':
                original_image = ContentFile(loyaltycard.image.read())
                now = datetime.now()
                digits = string.digits
                random_part = ''.join(random.choice(digits) for i in range(18))
                date_part = str(now.year) + str(now.month) + str(now.day) + '_' + str(now.hour) + str(now.minute) + str(now.second)
                image_copy_name = 'JPEG_' + date_part + '_' + random_part + '.jpg'
                loyaltycard.image.save(image_copy_name, original_image)
            loyaltycard.owner = user_to_share
            loyaltycard.save()
            data['usernameFrom'] = loyaltycard.owner.username
            data['usernameTo'] = user_to_share.username
            data['loyaltycardID'] = loyaltycard.pk
            send_notification(user_to_share, request.user, loyaltycard.title)
        except Account.DoesNotExist:
            data['detail'] = "User with username: " + username + " doesn't exist"
            return Response(data)
        except Exception as e:
            data['detail'] = str(e)
            return Response(data)
    else:
        data['detail'] = "You don't have permission"
    return Response(data)


def send_notification(user_to_send, user_from, loyaltycard_title):
    push_service = FCMNotification(FIREBASE_API_KEY)
    registration_id = user_to_send.device_registration_token
    message_title = loyaltycard_title
    message_body = user_from.username + ' send you his loyalty card!'
    extra_notification_kwargs = {
    'image': 'https://shopassist.azurewebsites.net/logo/'
    }
    try:
        push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, extra_notification_kwargs=extra_notification_kwargs)
    except:
        # exception when user_to_share is not logged in anywhere
        pass

