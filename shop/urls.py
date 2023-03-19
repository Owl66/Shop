from . import views
from django.urls import re_path

app_name = 'shop'
urlpatterns = [
    re_path(r'^what-is-happening/$', views.currently, name='currently'),
    re_path(r'^create-product/', views.createProduct, name='createProduct'),
    re_path(r'^like/$', views.productLike, name='productLike'), 
    re_path(r'^$', views.product_list, name='productList'),
    re_path(r'^delete-product/(?P<id>\d+)/$', views.deleteProduct, name='deleteProduct'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='productDetail'),
    re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='productListByCategory'),
]
