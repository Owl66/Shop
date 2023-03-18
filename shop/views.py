from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender, r
from .forms import PostForm
from actions.utils import create_action
from actions.models import Action
from .utils import is_ajax

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
def createProduct(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            create_action(request.user, 'has new product available for you!')
            return redirect(reverse('shop:productDetail', args=[post.id, post.slug]))
    else:
        form = PostForm()
    return render(request, 'shop/product/createProduct.html', {'form': form})

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

@login_required
def deleteProduct(request, id):
    if request.method == 'POST':
        if request.user.is_authenticated:
            post = get_object_or_404(Product, id=id)
            post.delete()
            create_action(request.user, 'has remove their product.')
            return redirect("/")
    return render(request, 'shop/product/deleteProduct.html')

@login_required
def currently(request):
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids).select_related('user', 'user__profile').prefetch_related('target')
        actions = actions[:10]
    return render(request, 'shop/product/currently.html', {'actions' : actions})