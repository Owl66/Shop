from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CouponApplyForm
from .models import Coupons

@login_required
@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupons.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            request.session['coupon_id'] = coupon.id
        except Coupons.DoesNotExist:
            request.session['coupon_id'] = None
            messages.info(request, "The coupon code is not available yet!")
    return redirect('cart:cartDetail')
    