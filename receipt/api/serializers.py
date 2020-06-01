from rest_framework import serializers
from receipt.models import Receipt

class ReceiptSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Receipt
        fields = ['id', 'title', 'shop_name', 'purchase_date', 'purchase_cost', 'return_time', 'warranty_time', 'image', 'owner']