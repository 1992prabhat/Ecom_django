from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from django.shortcuts import get_object_or_404
from .cart import Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from users.models import Address
from django.shortcuts import redirect
from orders.services import create_order

# Create your views here.
@login_required
def cart_add(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product, quantity)
        amount = cart.__len__()
        return JsonResponse({'message': 'Product added to cart successfully.', 'amount': amount})

@login_required
def remove_from_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart.remove(product_id)
        return JsonResponse({'message': 'Product removed from cart successfully.'})

@login_required
def update_cart(request):
    cart = Cart(request)
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        cart.update(product_id, quantity)
        return JsonResponse({'message': 'Cart updated successfully.'})

@login_required
def cart_overview(request):
    cart = Cart(request)
    return render(request, 'cart/cart_overview.html', {'cart': cart})

@login_required
def checkout(request):
    cart = Cart(request)
    if cart.is_empty():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart:cart_overview")

    addresses = (
        request.user.address_set
        .all()
        .order_by("-default", "-id")
    )

    if not addresses.exists():
        messages.info(
            request,
            "Please add a delivery address before checking out."
        )
        return redirect(
            f"{reverse('users:add_address')}?next={reverse('cart:checkout')}"
        )

    if request.method == "POST":
        address_id = request.POST.get("address")
        payment_method = request.POST.get("payment_method")

        try:
            address = request.user.address_set.get(id=address_id)
        except Address.DoesNotExist:
            messages.error(request, "Invalid delivery address.")
            return redirect("cart:checkout")

        try:
            order = create_order(
                user=request.user,
                address=address,
                payment_method=payment_method,
                cart=cart,
            )

        except ValueError as e:
            messages.error(request, str(e))
            return redirect("cart:checkout")


        cart.clear()

        messages.success(
            request,
            "Your order has been placed successfully."
        )

        return redirect(
            "orders:order_success",
            order_id=order.pk,
        )

    return render(
        request,
        "cart/checkout.html",
        {
            "cart": cart,
            "addresses": addresses,
        },
    )
