from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender, r
from .forms import PostForm

@login_required
def product_detail(request, id, slug):
    re = Recommender()
    product = get_object_or_404(Product, id=id,slug=slug, available=True)
    product_views = re.get_number_of_views(product)
    cart_product_form = CartAddProductForm()
    recommended_products = re.suggest_products_for([product], 6)
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        'recommended_products': recommended_products,
        'product_views': product_views,
    }
    return render(request, 'shop/product/detail.html', context)


@login_required
def createPost(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()
    return render(request, 'shop/product/createPost.html', {'form': form})
            

#Function to check for ajax request.
def is_ajax(request):
    return request.headers.get('X-Requested-With')=='XMLHttpRequest'

#Infinity scrolling using ajax
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all().filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        if is_ajax(request):
            return HttpResponse('<p>No more results</p>')
        products = paginator.page(paginator.num_pages)
    if is_ajax(request):
        context = {
           'categories': categories,
            'category' : category,
            'products' : products,
        }
        return render(request, 'shop/product/list_ajax.html', context)
    context = {
        'categories': categories,
        'category' : category,
        'products' : products,     
    }
    return render(request, 'shop/product/list.html', context)