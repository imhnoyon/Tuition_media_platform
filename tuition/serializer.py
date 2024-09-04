from rest_framework import serializers
from .models import Tuition,Review

class TuitionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tuition
        fields='__all__'


class ReviewSerializer(serializers.ModelSerializer):   
    class Meta:
        model=Review
        fields='__all__'

        