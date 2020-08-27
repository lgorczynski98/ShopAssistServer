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


class UsernameInfo():
    def __init__(self, username):
        self.username = username

class EmailInfo():
    def __init__(self, email):
        self.email = email

class PasswordInfo():
    def __init__(self, password, new_password):
        self.password = password
        self.new_password = new_password


class UsernameInfoSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return UsernameInfo(**validated_data)

class EmailInfoSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        return EmailInfo(**validated_data)

class PasswordInfoSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)
    new_password = serializers.CharField(max_length=30)

    def create(self, validated_data):
        return PasswordInfo(**validated_data)