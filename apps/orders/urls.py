
from django.urls import path
from . import views

app_name = 'orders'
urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
]
