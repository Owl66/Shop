from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^create/$', views.order_create, name='orderCreate'),
    re_path(r'^admin/order/(?P<order_id>\d+)/$', views.admin_order_detail, name='adminOrderDetail'),
    re_path(r'^admin/order/(?P<order_id>\d+)/pdf/$', views.admin_order_pdf, name='adminOrderPdf'),
]