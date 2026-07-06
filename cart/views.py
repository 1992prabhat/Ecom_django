from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product
from django.shortcuts import get_object_or_404
from .cart import Cart

# Create your views here.
def cart_add(request):
		cart = Cart(request)
		if request.method == 'POST':
				product_id = request.POST.get('product_id')
				product = get_object_or_404(Product, id=product_id)
				quantity = int(request.POST.get('quantity', 1))
				cart.add(product, quantity)
				amount = cart.__len__()
				return JsonResponse({'message': 'Product added to cart successfully.', 'amount': amount})

def remove_from_cart(request):
		cart = Cart(request)
		if request.method == 'POST':
				product_id = request.POST.get('product_id')
				cart.remove(product_id)
				return JsonResponse({'message': 'Product removed from cart successfully.'})

def update_cart(request):
		cart = Cart(request)
		if request.method == 'POST':
				product_id = request.POST.get('product_id')
				quantity = int(request.POST.get('quantity', 1))
				cart.update(product_id, quantity)
				return JsonResponse({'message': 'Cart updated successfully.'})


def cart_overview(request):
		cart = Cart(request)
		return render(request, 'cart/cart_overview.html', {'cart': cart})