
from rest_framework import serializers

from app.stores.models import Box

class BoxSerializer(serializers.ModelSerializer):
    """
    Creation and list Viewsets serializer for Box model
    """
    class Meta(object):
        model = Box
        fields = ('id', 'length', 'breadth', 'height')
        read_only_fields = ('id', )