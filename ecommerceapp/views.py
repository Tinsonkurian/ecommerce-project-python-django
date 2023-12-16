from django.shortcuts import get_object_or_404, redirect, render
from . models import Category, Products, Cart, CartItem
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
    allCategory = Category.objects.all()
    allProducts = Products.objects.all()
    paginator = Paginator(allProducts,3)
    try:
        page = int(request.GET.get('page','1'))
    except:
        page=1
    try:
        pageproducts = paginator.page(page)
    except (EmptyPage,InvalidPage):
        pageproducts=paginator.page(paginator.num_pages)
 
    return render(request, 'index.html', locals())

def category(request,catid):
    allCategory = Category.objects.all()
    categoryname = Category.objects.filter(id=catid)
    catname = Products.objects.filter(category=catid).values('name')
    productscat = Products.objects.filter(category=catid)
    return render(request, 'category.html', locals())

def details(request,proid):
    allCategory = Category.objects.all()
    product = Products.objects.get(id=proid)

    return render(request, 'prodetails.html',locals())

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    product = Products.objects.get(id = product_id)
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = CartItem.objects.get(product = product, cart = cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart
        )
        cart_item.save()
    return redirect('cart_detail')

def cart_detail(request,total=0,counter=0,cart_item=None):
    allCategory = Category.objects.all()

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',locals())

def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def full_remove(request, product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Products, id = product_id)
    cart_item = CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart_detail')



def search(request):
    allCategory = Category.objects.all()
    if request.method == 'POST':
        query = request.POST['search']
        products = Products.objects.filter(name__contains=query)
    return render(request, 'search.html', locals())