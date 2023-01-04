from rest_framework import serializers
from .models import Url

"""
Serializer for the Url model.
"""


class UrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = Url
        fields = ['original_url']
