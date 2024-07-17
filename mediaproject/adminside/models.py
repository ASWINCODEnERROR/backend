import uuid
from django.db import models
from django.contrib.auth.models import User  # Import User model from Django auth

class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ProductID = models.BigIntegerField(unique=True)
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = models.FileField(upload_to="uploads/", blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey(User, related_name="user_products", on_delete=models.CASCADE)
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    HSNCode = models.CharField(max_length=255, blank=True, null=True)
    TotalStock = models.DecimalField(default=0.00, max_digits=20, decimal_places=8, blank=True, null=True)

    def __str__(self):
        return self.ProductName

class SizeOption(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class ColorOption(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Products, related_name='variants', on_delete=models.CASCADE)
    size = models.ForeignKey(SizeOption, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorOption, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    sku = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return f'{self.product.ProductName} - {self.size.name} - {self.color.name}'