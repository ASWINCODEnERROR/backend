from django.urls import path,re_path
from .views import ProductListCreateView, ProductDetailView, DecrementStockView, ProductVariantDetailView,ProductVariantCreateView,SizeOptionListView,ColorOptionListView,ProductVariantBulkCreateView,ProductListView
from . import views

urlpatterns = [

    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<uuid:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('size-options/', SizeOptionListView.as_view(), name='size-options'),
    path('color-options/', ColorOptionListView.as_view(), name='color-options'),
    path('product-variants/bulk_create/', ProductVariantBulkCreateView.as_view(), name='product-variant-bulk-create'),
    path('productslist/', ProductListView.as_view(), name='product-list'),
    re_path(r'^productslist/(?P<productId>[\w-]+)/$', views.product_detail_view, name='product_detail'),
    path('decrement-stock/<int:variant_id>/', DecrementStockView.as_view(), name='decrement-stock'),


    ]