
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product
from .forms import ProductForm

def home_view(request):
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:12]
    return render(request, 'home.html', {'products': products})

def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'product_list.html', {'products': products})

@login_required
def add_product_view(request):
    if request.user.role != 'seller':
        messages.error(request, 'শুধু বিক্রেতারা পণ্য যোগ করতে পারেন।')
        return redirect('home')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, 'পণ্য সফলভাবে যুক্ত হয়েছে।')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_add.html', {'form': form})

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'product_detail.html', {'product': product})
