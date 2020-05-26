# from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.parsers import JSONParser

# from loyaltycard.models import Loyaltycard
# from loyaltycard.api.serializers import LoyaltycardSerializer

# @csrf_exempt
# def loyaltycard_list(request):
#     if request.method == 'GET':
#         loyaltycards = Loyaltycard.objects.all()
#         serializer = LoyaltycardSerializer(loyaltycards, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = LoyaltycardSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def loyaltycard_detail(request, pk):
#     try:
#         loyaltycard = Loyaltycard.objects.get(pk=pk)
#     except Loyaltycard.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = LoyaltycardSerializer(loyaltycard)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = LoyaltycardSerializer(loyaltycard, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         loyaltycard.delete()
#         return HttpResponse(status=204)

from loyaltycard.models import Loyaltycard
from loyaltycard.api.serializers import LoyaltycardSerializer
from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes((IsAuthenticated,))
class LoyaltycardList(generics.ListCreateAPIView):
    queryset = Loyaltycard.objects.all()
    serializer_class = LoyaltycardSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LoyaltycardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loyaltycard.objects.all()
    serializer_class = LoyaltycardSerializer
    def perform_destroy(self, instance):
        if instance.owner == self.request.user:
            instance.delete()