from loyaltycard.models import Loyaltycard
from loyaltycard.api.serializers import LoyaltycardSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
            instance.delete()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.owner == self.request.user:
            serializer.save()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.owner == self.request.user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response(status=403)

