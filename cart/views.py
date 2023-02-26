from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from shop.models import Product
from .forms import CartAddProductForm
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender

@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cartDetail')

@login_required
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if cart:
        return redirect('cart:cartDetail')
    return redirect('/')

@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    coupon_apply_form = CouponApplyForm()
    r = Recommender()
    cart_products = [item['product'] for item in cart]
    recommended_products = r.suggest_products_for(cart_products, max_results=4)
    context = {
        'cart': cart, 
        'coupon_apply_form':coupon_apply_form,
        'recommended_products':recommended_products,
   }
    return render(request, 'cart/detail.html', context)

