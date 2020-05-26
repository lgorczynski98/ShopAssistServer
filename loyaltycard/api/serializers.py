from rest_framework import serializers
from loyaltycard.models import Loyaltycard

class LoyaltycardSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Loyaltycard
        fields = ['id', 'title', 'barcode_format', 'barcode_content', 'image_url', 'owner']
        