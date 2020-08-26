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


class ProfilesInfo():
    def __init__(self, username=None, email=None, password=None):
        self.username = username or None
        self.email = email or None
        self.password = password or None


class ProfilesInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(max_length=30, required=False)

    def create(self, validated_data):
        return ProfilesInfo(**validated_data)
