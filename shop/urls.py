from . import views
from django.urls import re_path

app_name = 'shop'
urlpatterns = [
    re_path(r'^create-post/', views.createPost, name='createPost'), 
    re_path(r'^$', views.product_list, name='productList'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='productDetail'),
    re_path(r'^(?P<category_slug>[-\w]+)/$', views.product_list, name='productListByCategory'),
]
