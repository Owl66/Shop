from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .forms import OrderCreateForm
from .models import OrderItem
from .models import Order
from cart.cart import Cart
from django.conf import settings
from django.http import HttpResponse 
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import weasyprint

@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            cd = form.cleaned_data
            email = cd['email']
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], 
                                        quantity=item['quantity'])
            cart.clear()
            return render(request, 'orders/order/created.html', {'order':order, 'email':email})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart, 'form':form})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})


    