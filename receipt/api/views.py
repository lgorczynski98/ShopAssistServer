from receipt.models import Receipt
from receipt.api.serializers import ReceiptSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view
import os

@permission_classes((IsAuthenticated,))
class ReceiptList(generics.ListCreateAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = Receipt.objects.filter(owner=request.user)
        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        

@permission_classes((IsAuthenticated,))
class ReceiptDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            os.remove(instance.image.path)
            if instance.image.name != 'thumbnail/default.jpg':
                os.remove(instance.thumbnail.path)
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
def get_receipt_image(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    if receipt.owner == request.user:
        img = open(receipt.image.path, 'rb')
        response = FileResponse(img)
        return response
    data = {}
    data['detail'] = "You don't have permission"
    return Response(data, status=403)


@permission_classes((IsAuthenticated,))
@api_view(['GET',])
def get_thumbnail_image(request, receipt_id):
    receipt = Receipt.objects.get(id=receipt_id)
    if receipt.owner == request.user:
        img = open(receipt.thumbnail.path, 'rb')
        response = FileResponse(img)
        return response
    data = {}
    data['detail'] = "You don't have permission"
    return Response(data, status=403)