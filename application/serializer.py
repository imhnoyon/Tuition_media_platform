from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    # teacher=serializers.SlugRelatedField(many=False)
    class Meta:
        model=Application
        fields='__all__'
