from rest_framework import serializers

from django.contrib.auth.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['is_superuser'] = user.is_superuser
        data['id']=user.id
     
        return data
from rest_framework import serializers
from .models import Products, ProductVariant, SizeOption, ColorOption

class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = '__all__'

class ColorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorOption
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeOptionSerializer()
    color = ColorOptionSerializer()

    class Meta:
        model = ProductVariant
        fields = '__all__'

    def create(self, validated_data):
        size_data = validated_data.pop('size')
        color_data = validated_data.pop('color')

        # Assuming SizeOption and ColorOption are related fields on ProductVariant
        size_instance = SizeOption.objects.create(**size_data)
        color_instance = ColorOption.objects.create(**color_data)

        variant = ProductVariant.objects.create(
            size=size_instance,
            color=color_instance,
            **validated_data
        )

        return variant

class ProductsSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = '__all__'
class SizeOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = '__all__'

class ColorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorOption
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    size = serializers.PrimaryKeyRelatedField(queryset=SizeOption.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=ColorOption.objects.all())

    class Meta:
        model = ProductVariant
        fields = '__all__'







# new
class SizeOptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizeOption
        fields = '__all__'

class ColorOptionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ColorOption
        fields = '__all__'

class ProductVariantDetailSerializer(serializers.ModelSerializer):
    size = SizeOptionDetailSerializer()
    color = ColorOptionDetailSerializer()

    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductVariantCreateSerializer(serializers.ModelSerializer):
    size = serializers.PrimaryKeyRelatedField(queryset=SizeOption.objects.all())
    color = serializers.PrimaryKeyRelatedField(queryset=ColorOption.objects.all())

    class Meta:
        model = ProductVariant
        fields = '__all__'

class ProductVariantDetailSerializer(serializers.ModelSerializer):
    size = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ('id', 'size', 'color', 'stock', 'sku')

    def get_size(self, obj):
        return obj.size.name if obj.size else None

    def get_color(self, obj):
        return obj.color.name if obj.color else None

class ProductDetailSerializer(serializers.ModelSerializer):
    variants = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = ('id', 'ProductID', 'ProductCode', 'ProductName', 'ProductImage', 'CreatedDate', 'UpdatedDate', 
                  'CreatedUser', 'IsFavourite', 'Active', 'HSNCode', 'TotalStock', 'variants')

    def get_variants(self, obj):
        variants = obj.variants.all()
        if variants.exists():
            return ProductVariantDetailSerializer(variants, many=True).data
        else:
            return None