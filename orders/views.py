from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order
from django.shortcuts import get_object_or_404


# Create your views here.
@login_required
def order_success(request, order_id):
	if not order_id:
		return redirect('cart:checkout')

	order = get_object_or_404(Order, id=order_id, user=request.user)
	return render(request, 'orders/order_success.html', {'order': order})

@login_required
def all_orders(request):
	orders = (
		Order.objects
		.filter(user=request.user)
		.prefetch_related("items")
		.order_by("-created_at")
	)
	return render(request, 'orders/all_orders.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items__product"),
        id=order_id,
        user=request.user,
    )

    return render(
        request,
        "orders/order_details.html",
		{
			"order": order,
		},
	)