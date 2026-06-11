import os

# প্রোজেক্ট রুট
BASE_DIR = os.getcwd()

# ফোল্ডার তৈরি
folders = [
    'hifive_shop',
    'apps/accounts',
    'apps/products',
    'apps/orders',
    'templates',
    'static/css',
    'media'
]
for f in folders:
    os.makedirs(os.path.join(BASE_DIR, f), exist_ok=True)

# settings.py
settings_content = '''
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-8@^_=k%m1q7x0p9lz#2!n$b(5r&v*e+f+g+h+i+j+k+l+m+n+o+p'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'crispy_bootstrap5',
    'apps.accounts',
    'apps.products',
    'apps.orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hifive_shop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.products.context_processors.categories_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'hifive_shop.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'bn'
TIME_ZONE = 'Asia/Dhaka'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
PAYMENT_DUMMY_SUCCESS = True
'''
with open('hifive_shop/settings.py', 'w') as f:
    f.write(settings_content)

# urls.py
urls_content = '''
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.products.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('orders/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
with open('hifive_shop/urls.py', 'w') as f:
    f.write(urls_content)

# অন্যান্য hifive_shop ফাইল
with open('hifive_shop/__init__.py', 'w') as f:
    f.write('')
with open('hifive_shop/wsgi.py', 'w') as f:
    f.write('import os\nfrom django.core.wsgi import get_wsgi_application\nos.environ.setdefault("DJANGO_SETTINGS_MODULE", "hifive_shop.settings")\napplication = get_wsgi_application()')
with open('hifive_shop/asgi.py', 'w') as f:
    f.write('import os\nfrom django.core.asgi import get_asgi_application\nos.environ.setdefault("DJANGO_SETTINGS_MODULE", "hifive_shop.settings")\napplication = get_asgi_application()')

# manage.py
manage_content = '''#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hifive_shop.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Couldn't import Django")
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
'''
with open('manage.py', 'w') as f:
    f.write(manage_content)

# apps/accounts/models.py
with open('apps/accounts/models.py', 'w') as f:
    f.write('''
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('buyer', 'ক্রেতা'), ('seller', 'বিক্রেতা'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
''')

# apps/accounts/views.py
with open('apps/accounts/views.py', 'w') as f:
    f.write('''
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'ইউজারনেম বা পাসওয়ার্ড ভুল')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
''')

# apps/accounts/forms.py
with open('apps/accounts/forms.py', 'w') as f:
    f.write('''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, initial='buyer')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'phone', 'address', 'role')
''')

# apps/accounts/urls.py
with open('apps/accounts/urls.py', 'w') as f:
    f.write('''
from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
''')

# apps/accounts/__init__.py, admin.py, apps.py
for file in ['__init__.py', 'admin.py', 'apps.py']:
    with open(f'apps/accounts/{file}', 'w') as f:
        f.write('')

# apps/products/models.py
with open('apps/products/models.py', 'w') as f:
    f.write('''
from django.db import models
from apps.accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'seller'})
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/')
    shipping_details = models.TextField(help_text="ডেলিভারি খরচ, সময়, কুরিয়ার")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    def __str__(self): return self.name
''')

# apps/products/views.py
with open('apps/products/views.py', 'w') as f:
    f.write('''
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
''')

# apps/products/forms.py
with open('apps/products/forms.py', 'w') as f:
    f.write('''
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'price', 'stock', 'image', 'shipping_details']
''')

# apps/products/urls.py
with open('apps/products/urls.py', 'w') as f:
    f.write('''
from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('add/', views.add_product_view, name='add_product'),
    path('<int:pk>/', views.product_detail_view, name='product_detail'),
]
''')

# apps/products/context_processors.py
with open('apps/products/context_processors.py', 'w') as f:
    f.write('''
from .models import Category
def categories_processor(request):
    return {'all_categories': Category.objects.all()}
''')

for file in ['__init__.py', 'admin.py', 'apps.py']:
    with open(f'apps/products/{file}', 'w') as f:
        f.write('')

# apps/orders/models.py
with open('apps/orders/models.py', 'w') as f:
    f.write('''
from django.db import models
from apps.accounts.models import User
from apps.products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='Pending')
    order_status = models.CharField(max_length=20, default='Processing')
    shipping_address = models.TextField()
    transaction_id = models.CharField(max_length=100, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
''')

# apps/orders/views.py
with open('apps/orders/views.py', 'w') as f:
    f.write('''
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
''')

# apps/orders/urls.py
with open('apps/orders/urls.py', 'w') as f:
    f.write('''
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
''')

for file in ['__init__.py', 'admin.py', 'apps.py']:
    with open(f'apps/orders/{file}', 'w') as f:
        f.write('')

# Templates
templates = {
    'base.html': '''<!DOCTYPE html><html lang="bn"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HiFive Shop</title><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"></head><body><nav class="navbar navbar-expand-lg navbar-dark bg-dark"><div class="container"><a class="navbar-brand" href="/">HiFive Shop</a><button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"><span class="navbar-toggler-icon"></span></button><div class="collapse navbar-collapse" id="navbarNav"><ul class="navbar-nav me-auto"><li class="nav-item"><a class="nav-link" href="{% url 'products:product_list' %}">সব পণ্য</a></li>{% if user.is_authenticated and user.role == 'seller' %}<li class="nav-item"><a class="nav-link" href="{% url 'products:add_product' %}">পণ্য যোগ করুন</a></li>{% endif %}<li class="nav-item"><a class="nav-link" href="{% url 'orders:cart' %}">🛒 কার্ট</a></li></ul><ul class="navbar-nav">{% if user.is_authenticated %}<li class="nav-item"><span class="nav-link">স্বাগতম, {{ user.username }}</span></li><li class="nav-item"><a class="nav-link" href="{% url 'accounts:logout' %}">লগআউট</a></li>{% else %}<li class="nav-item"><a class="nav-link" href="{% url 'accounts:login' %}">লগইন</a></li><li class="nav-item"><a class="nav-link" href="{% url 'accounts:register' %}">রেজিস্টার</a></li>{% endif %}</ul></div></div></nav><div class="container mt-4">{% if messages %}{% for message in messages %}<div class="alert alert-{{ message.tags }}">{{ message }}</div>{% endfor %}{% endif %}{% block content %}{% endblock %}</div><footer class="bg-light text-center p-3 mt-5"><small>© 2026 HiFive Shop</small></footer><script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script></body></html>''',
    'home.html': '''{% extends 'base.html' %}{% block content %}<div class="jumbotron bg-light p-5 rounded mb-4"><h1>HiFive Shop-এ স্বাগতম</h1><p>প্রাকৃতিক ও চামড়াজাত পণ্যের সেরা ঠিকানা</p><a href="{% url 'products:product_list' %}" class="btn btn-primary">ব্রাউজ করুন</a></div><h3>সর্বশেষ পণ্য</h3><div class="row">{% for product in products %}<div class="col-md-3 mb-4"><div class="card h-100"><img src="{{ product.image.url }}" class="card-img-top" style="height:200px; object-fit:cover;"><div class="card-body"><h5 class="card-title">{{ product.name }}</h5><p class="card-text">টাকা {{ product.price }}</p><a href="{% url 'products:product_detail' product.id %}" class="btn btn-sm btn-outline-primary">বিস্তারিত</a><a href="{% url 'orders:add_to_cart' product.id %}" class="btn btn-sm btn-success">কার্টে যোগ</a></div></div></div>{% endfor %}</div>{% endblock %}''',
    'product_list.html': '''{% extends 'base.html' %}{% block content %}<h2>সব পণ্য</h2><div class="row">{% for product in products %}<div class="col-md-3 mb-4"><div class="card"><img src="{{ product.image.url }}" class="card-img-top" height="180" style="object-fit:cover;"><div class="card-body"><h6>{{ product.name|truncatechars:30 }}</h6><strong>{{ product.price }} টাকা</strong><p class="small">{{ product.shipping_details|truncatewords:8 }}</p><a href="{% url 'orders:add_to_cart' product.id %}" class="btn btn-sm btn-warning">কার্টে নিন</a></div></div></div>{% empty %}<p>কোনো পণ্য পাওয়া যায়নি।</p>{% endfor %}</div>{% endblock %}''',
    'product_add.html': '''{% extends 'base.html' %}{% load crispy_forms_tags %}{% block content %}<h2>নতুন পণ্য যোগ করুন</h2><form method="post" enctype="multipart/form-data">{% csrf_token %}{{ form|crispy }}<button type="submit" class="btn btn-success">যোগ করুন</button></form>{% endblock %}''',
    'product_detail.html': '''{% extends 'base.html' %}{% block content %}<div class="row"><div class="col-md-6"><img src="{{ product.image.url }}" class="img-fluid"></div><div class="col-md-6"><h2>{{ product.name }}</h2><p>{{ product.description }}</p><h4>টাকা {{ product.price }}</h4><p><strong>শিপিং:</strong> {{ product.shipping_details }}</p><a href="{% url 'orders:add_to_cart' product.id %}" class="btn btn-primary">কার্টে যোগ করুন</a></div></div>{% endblock %}''',
    'cart.html': '''{% extends 'base.html' %}{% block content %}<h2>আপনার কার্ট</h2><table class="table"><thead><tr><th>পণ্য</th><th>দাম</th><th>পরিমাণ</th><th>মোট</th><th></th></tr></thead><tbody>{% for item in items %}<tr><td>{{ item.product.name }}</td><td>{{ item.product.price }}</td><td>{{ item.quantity }}</td><td>{% widthratio item.product.price 1 item.quantity %}</td><td><a href="{% url 'orders:remove_from_cart' item.id %}" class="btn btn-sm btn-danger">সরান</a></td></tr>{% empty %}<tr><td colspan="5">কার্ট খালি</td></tr>{% endfor %}</tbody><tfoot><tr><td colspan="3"><strong>সর্বমোট</strong></td><td><strong>{{ total }}</strong></td><td></td></tr></tfoot></table><a href="{% url 'orders:checkout' %}" class="btn btn-primary">অর্ডার সম্পন্ন</a>{% endblock %}''',
    'checkout.html': '''{% extends 'base.html' %}{% block content %}<h2>ঠিকানা ও পেমেন্ট</h2><form method="post">{% csrf_token %}<div class="mb-3"><label>ডেলিভারি ঠিকানা</label><textarea name="address" class="form-control" required></textarea></div><p>মোট পরিশোধ্য: <strong>{{ total }} টাকা</strong></p><button type="submit" class="btn btn-success">ডামি পেমেন্ট করুন</button><p class="text-muted mt-2">⚠️ ডেমো মোড: পেমেন্ট ছাড়াই অর্ডার কনফার্ম হবে।</p></form>{% endblock %}''',
    'order_success.html': '''{% extends 'base.html' %}{% block content %}<div class="alert alert-success"><h3>অর্ডার সফল হয়েছে!</h3><p>অর্ডার আইডি: {{ order.id }} | ট্রানজেকশন আইডি: {{ order.transaction_id }}</p><p>আপনার অর্ডারটি প্রক্রিয়াধীন। ধন্যবাদ।</p><a href="/" class="btn btn-primary">হোমপেজে যান</a></div>{% endblock %}''',
    'login.html': '''{% extends 'base.html' %}{% block content %}<h2>লগইন</h2><form method="post">{% csrf_token %}<input type="text" name="username" class="form-control mb-2" placeholder="ইউজারনেম"><input type="password" name="password" class="form-control mb-2" placeholder="পাসওয়ার্ড"><button type="submit" class="btn btn-primary">প্রবেশ</button></form>{% endblock %}''',
    'register.html': '''{% extends 'base.html' %}{% load crispy_forms_tags %}{% block content %}<h2>রেজিস্ট্রেশন</h2><form method="post">{% csrf_token %}{{ form|crispy }}<button type="submit" class="btn btn-success">একাউন্ট খুলুন</button></form>{% endblock %}'''
}
for name, content in templates.items():
    with open(f'templates/{name}', 'w') as f:
        f.write(content)

# requirements.txt
with open('requirements.txt', 'w') as f:
    f.write('Django==5.0.3\nPillow==10.2.0\ndjango-crispy-forms==2.1\ncrispy-bootstrap5==0.7\n')

print("✅ সব ফাইল সফলভাবে তৈরি হয়েছে!")
