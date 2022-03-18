from rest_framework import serializers

from main.models import Ad, Category


class AdSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ad
