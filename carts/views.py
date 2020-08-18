from django.shortcuts import render
from .models import Cart
from django.shortcuts import redirect
from products.models import Product
from .utils import get_or_create_cart
from django.shortcuts import get_object_or_404
# Create your views here.
def cart(request):
    #request.session['cart_id'] =  None
    cart = get_or_create_cart(request)
    return render (request,'carts/cart.html',{
        'cart':cart
    })
def add(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))

    cart.products.add(product)
    return render(request,'carts/add.html',{
        'product': product
    })
def remove(request):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=request.POST.get('product_id'))
    cart.products.remove(product)
    return redirect('carts:cart')
