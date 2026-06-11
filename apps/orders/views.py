
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Cart, CartItem, Order, OrderItem
from apps.products.models import Product

def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

@login_required
def cart_view(request):
    cart = get_or_create_cart(request.user)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    messages.success(request, f'{product.name} কার্টে যোগ হয়েছে')
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart')

@login_required
def checkout_view(request):
    cart = get_or_create_cart(request.user)
    items = CartItem.objects.filter(cart=cart)
    if not items:
        return redirect('cart')
    total = sum(item.product.price * item.quantity for item in items)

    if request.method == 'POST':
        address = request.POST.get('address')
        order = Order.objects.create(
            buyer=request.user,
            total_amount=total,
            payment_status='Paid' if settings.PAYMENT_DUMMY_SUCCESS else 'Pending',
            order_status='Confirmed',
            shipping_address=address,
            transaction_id=''
        )
        order.transaction_id = f"DUMMY_{order.id}"
        order.save()
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        items.delete()
        messages.success(request, 'অর্ডার সফল হয়েছে! পেমেন্ট ডামি মোডে সম্পন্ন।')
        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {'total': total})

@login_required
def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    return render(request, 'order_success.html', {'order': order})
