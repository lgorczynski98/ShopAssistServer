from loyaltycard.models import Loyaltycard
from account.models import Account
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    loyaltycards = serializers.PrimaryKeyRelatedField(many=True, queryset=Loyaltycard.objects.all())
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'loyaltycards', 'device_registration_token']


class RegistrationSerializer(serializers.ModelSerializer):
    loyaltycards = serializers.PrimaryKeyRelatedField(many=True, queryset=Loyaltycard.objects.all())

    class Meta:
        model = Account
        fields = ['email', 'username', 'password', 'loyaltycards']

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account
