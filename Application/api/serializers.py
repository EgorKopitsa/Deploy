from rest_framework import serializers

from ..models import Category, Top, Button, Shoes


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    slug = serializers.SlugField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug'
        ]


class BaseProductSerializer:

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects)
    title = serializers.CharField(required=True)
    slug = serializers.SlugField(required=True)
    image = serializers.ImageField(required=True)
    description = serializers.CharField(required=False)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    available = serializers.BooleanField(required=True)
    dimensions = serializers.CharField(required=True)


class TopSerializer(BaseProductSerializer, serializers.ModelSerializer):

    class Meta:
        model = Top
        fields = '__all__'


class ButtonSerializer(BaseProductSerializer, serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = '__all__'


class ShoesSerializer(BaseProductSerializer, serializers.ModelSerializer):

    class Meta:
        model = Shoes
        fields = '__all__'
