from django.urls import path
from .views import (
    HomeView, ProductDetailView, AddToCartView, 
    CartView, CheckoutView, OrderHistoryView, decrease_cart_item, increase_cart_item
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('product/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('add-to-cart/<int:product_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', CartView.as_view(), name='view_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('orders/', OrderHistoryView.as_view(), name='order_history'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/increase/<int:item_id>/', increase_cart_item, name='increase_cart_item'),
    path('cart/decrease/<int:item_id>/', decrease_cart_item, name='decrease_cart_item'),
]
