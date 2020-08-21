from .utils import breadcrumb
from .utils import destroy_order
from carts.utils import destroy_cart
from carts.utils import get_or_create_cart
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .utils import get_or_create_order
from .models import Order
from .mails import Mail
from shipping_addresses.models import ShippingAddress

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.list import ListView
from django.db.models.query import EmptyQuerySet
from .decorators import validate_cart_and_order


# Create your views here.

class OrderListView(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name = 'orders/orders.html'

    def get_queryset(self):
        return self.request.user.orders_completed()
@validate_cart_and_order
@login_required(login_url='login')
def order(request, cart, order):

    return render(request, 'orders/order.html',{
        'cart': cart,
        'order': order,
        'breadcrumb':breadcrumb()
    })
@validate_cart_and_order
@login_required(login_url='login')
def address(request, cart, order):


    #shipping_address = order.shipping_address
    shipping_address = order.get_or_set_shipping_address()
    can_choose_address = request.user.shippingaddress_set.count() > 1

    return render(request, 'orders/address.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'can_choose_address': can_choose_address,
        'breadcrumb': breadcrumb(address=True)
    })

@login_required(login_url='login')
def select_address(request):
    #shipping_addresses = request.user.addresses
    shipping_addresses = request.user.shippingaddress_set.all()

    return render(request, 'orders/select_address.html', {
        'breadcrumb': breadcrumb(address=True),
        'shipping_addresses': shipping_addresses
    })

@login_required(login_url='login')
@validate_cart_and_order
def check_address(request, cart, order, pk):
    shipping_address = get_object_or_404(ShippingAddress, pk=pk)

    if request.user.id != shipping_address.user_id:
        return redirect('carts:cart')

    order.update_shipping_address(shipping_address)

    return redirect('orders:address')

@validate_cart_and_order
@login_required(login_url='login')
def confirm(request, cart, order):
    cart = get_or_create_cart(request)
    order = get_or_create_order(cart, request)

#    if not cart.has_products() or order.shipping_address is None or order.billing_profile is None:
#        return redirect('carts:cart')

    shipping_address = order.shipping_address
    if shipping_address is None:
        return redirect('orders:address')

    return render(request, 'orders/confirm.html', {
        'cart': cart,
        'order': order,
        'shipping_address': shipping_address,
        'breadcrumb': breadcrumb(address=True, payment=True, confirmation=True)
    })
@validate_cart_and_order
@login_required(login_url='login')
def cancel(request, cart, order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.cancel()

    destroy_cart(request)
    destroy_order(request)

    messages.error(request, 'Orden cancelada')
    return redirect('index')

@validate_cart_and_order
@login_required(login_url='login')
def complete(request, cart, order):

    if request.user.id != order.user_id:
        return redirect('carts:cart')

    order.complete()
    Mail.send_complete_order(order, request.user)

    destroy_cart(request)
    destroy_order(request)

    messages.success(request, 'Compra completada exitosamente')
    return redirect('index')
