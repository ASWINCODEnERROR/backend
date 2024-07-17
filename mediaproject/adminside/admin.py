from django.contrib import admin
from .models import Products, SizeOption, ColorOption, ProductVariant

admin.site.register(Products)
admin.site.register(SizeOption)
admin.site.register(ColorOption)
admin.site.register(ProductVariant)