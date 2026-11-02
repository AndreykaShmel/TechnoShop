import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services.ai_advisor import get_advice
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'catalog/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        # Если quantity пустое, ставим 1
        quantity = cd['quantity'] if cd['quantity'] else 1
        cart.add(product=product, quantity=quantity, override_quantity=cd['override'])
    else:
        # Если форма невалидна, всё равно добавляем 1 штуку (на всякий случай)
        cart.add(product=product, quantity=1, override_quantity=False)

    return redirect('catalog:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('catalog:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    print(f"--- В КОРЗИНЕ СЕЙЧАС: {request.session.get('cart')} ---")
    return render(request, 'catalog/cart_detail.html', {'cart': cart})


from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            # Если пользователь авторизован, привязываем заказ к нему
            if request.user.is_authenticated:
                order.user = request.user
            order.total = cart.get_total_price()
            order.save()

            # Переносим товары из корзины в заказ
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            # Очищаем корзину
            cart.clear()

            # Перенаправляем на страницу успеха (передаем ID заказа)
            return redirect('catalog:order_success', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'catalog/order_create.html', {'cart': cart, 'form': form})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'catalog/order_success.html', {'order': order})
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Автоматически входим после регистрации
            return redirect('catalog:product_list')
    else:
        form = RegisterForm()
    return render(request, 'catalog/register.html', {'form': form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catalog/my_orders.html', {'orders': orders})


@require_POST
def ai_advice(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        data = json.loads(request.body)
        question = data.get('question', 'Расскажи об этом товаре')
    except:
        question = 'Расскажи об этом товаре'

    answer = get_advice(product, question)
    return JsonResponse({'answer': answer})