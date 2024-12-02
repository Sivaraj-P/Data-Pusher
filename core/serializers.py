from rest_framework import serializers
from .models import Account,Destination


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Account
        fields='__all__'
        read_only_fields=["secret_token"]


class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Destination
        fields='__all__'