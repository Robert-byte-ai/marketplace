from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from main.models import Ad, Category


class AdSerializer(serializers.ModelSerializer):
    category = SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    seller = serializers.StringRelatedField()

    class Meta:
        fields = (
            'seller',
            'pub_date',
            'category',
            'tags',
            'price',
            'text'
        )
        model = Ad
