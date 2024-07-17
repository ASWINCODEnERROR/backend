from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Products
from .serializers import ProductsSerializer
from django.db.models import F
from rest_framework import generics
from .models import Products, ProductVariant
from .serializers import ProductsSerializer, ProductVariantSerializer
from authentication.serializers import UserSerializer
from .serializers import SizeOptionSerializer, ColorOptionSerializer
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Products 
import uuid

# Create your views here.

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# class CustomTokenObtainPairView(TokenObtainPairView):
#     print("<<<<<<<<<<<<<<<<<<<<<<<<<<entering>>>>>>>>>>>>>>>>>>>>>>>>>>>")
#     def post(self, request, *args, **kwargs):
#         print("<<<<<<<<<<<<<<<<<<<<<<<<<<entering -00>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#         response = post(request, *args, **kwargs)
#         serializer = self.get_serializer(data=request.data)
#         print("<<<<<<<<<<<<<<<<<<<<<<<<<<entering>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#         serializer.is_valid(raise_exception=True)
#         user = serializer.user
#         refresh = RefreshToken.for_user(user)
#         access_token = str(response.data['access'])
#         print("<<<<<<<<<<<<<<<<<<<<<<<<<<entering>>>>>>>>>>>>>>>>>>>>>>>>>>>")

#         user_serializer = UserSerializer(user)
#         response.data['user'] = user_serializer.data  # Include serialized data, not the serializer object
#         return response


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        queryset = Products.objects.first()
        print(queryset.id)
        headers = self.get_success_headers(response.data)
        return Response({'createdid': queryset.pk,'name':queryset.ProductName}, status=status.HTTP_201_CREATED, headers=headers)
    


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

class ProductVariantListCreateView(generics.ListCreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer

class ProductVariantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer


class ProductVariantCreateView(generics.CreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantCreateSerializer

    def create(self, request, *args, **kwargs):
        # Extract relevant data from request
        product = request.data.get('product')
        size = request.data.get('size')
        color = request.data.get('color')

        # Check if the combination of product, size, and color already exists
        if ProductVariant.objects.filter(product=product, size=size, color=color).exists():
            return Response(
                {"non_field_errors": ["The fields product, size, color must make a unique set alredy avilabile."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If unique, proceed with creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class SizeOptionListView(generics.ListAPIView):
    queryset = SizeOption.objects.all()
    serializer_class = SizeOptionSerializer

class ColorOptionListView(generics.ListAPIView):
    queryset = ColorOption.objects.all()
    serializer_class = ColorOptionSerializer





class ProductVariantBulkCreateView(generics.CreateAPIView):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        product_id = request.data.get('product')
        variants = request.data.get('variants', [])

        try:
            product = Products.objects.select_for_update().get(id=product_id)  # Lock the product row for update
        except Products.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_variants = []
        errors = []

        for variant_data in variants:
            try:
                size_id = variant_data.get('size')
                color_id = variant_data.get('color')
                stock = variant_data.get('stock')
                sku = variant_data.get('sku')

                size = SizeOption.objects.get(id=size_id)
                color = ColorOption.objects.get(id=color_id)

                # Check if the variant already exists
                if ProductVariant.objects.filter(product=product, size=size, color=color).exists():
                    errors.append({
                        "error": f"Variant with size '{size_id}' and color '{color_id}' already exists for product '{product_id}'."
                    })
                else:
                    new_variants.append(ProductVariant(
                        product=product,
                        size=size,
                        color=color,
                        stock=stock,
                        sku=sku
                    ))
            except (SizeOption.DoesNotExist, ColorOption.DoesNotExist) as e:
                errors.append({
                    "error": f"Invalid size or color ID: {str(e)}"
                })

        if errors:
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        # Bulk create new variants
        ProductVariant.objects.bulk_create(new_variants)

        # Update Products TotalStock
        total_stock = ProductVariant.objects.filter(product=product).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
        product.TotalStock = total_stock
        product.save()

        return Response(
            {"message": "Variants created successfully"},
            status=status.HTTP_201_CREATED
        )


class ProductListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailSerializer


def product_detail_view(request, productId):
    try:
        product = get_object_or_404(Products, ProductID=productId)
    except ValueError:
        return JsonResponse({'error': 'Invalid UUID format'}, status=400)

    # Assuming you have a serializer or directly constructing JSON response
    data = {
        "id": str(product.ProductID),
        "ProductCode": product.ProductCode,
        "ProductName": product.ProductName,
        "ProductImage": request.build_absolute_uri(product.ProductImage.url),
        "CreatedDate": product.CreatedDate,
        "IsFavourite": product.IsFavourite,
        "Active": product.Active,
        "HSNCode": product.HSNCode,
        "TotalStock": str(product.TotalStock),
        "CreatedUser": product.CreatedUser.id,
        "variants": [
            {
                "id": variant.id,
                "size": {
                    "id": variant.size.id,
                    "name": variant.size.name,
                },
                "color": {
                    "id": variant.color.id,
                    "name": variant.color.name,
                },
                "stock": variant.stock,
                "sku": variant.sku,
                "product": str(product.ProductID),
            }
            for variant in product.variants.all()  # Assuming you have a related_name 'variants' for variants in Product model
        ]
    }
    return JsonResponse(data)


class DecrementStockView(APIView):
    
    def patch(self, request, variant_id):
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        if variant.stock > 0:
            variant.stock -= 1
            variant.save()

            # Update TotalStock for the related product
            product = variant.product
            total_stock = ProductVariant.objects.filter(product=product).aggregate(total_stock=Sum('stock'))['total_stock'] or 0
            product.TotalStock = total_stock
            product.save()

            serializer = ProductVariantSerializer(variant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Stock is already zero"}, status=status.HTTP_400_BAD_REQUEST)


# ******************************************************************************************************