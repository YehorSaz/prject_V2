from rest_framework import serializers

from apps.currencies.models import CurrenciesModel


class CurrenciesSerializer(serializers.Serializer):
    class Meta:
        model = CurrenciesModel
        fields = ('EUR', 'USD', 'created_at', 'updated_at')
        