from decimal import Decimal
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product

def create_order(*, user, address, payment_method, cart):
    """
    Creates an order from the session cart.

    Raises:
        ValueError: If any product has insufficient stock.
    """

    cart_items = []
    order_total = Decimal('0.00')
    for item in cart:
        product = item['product']
        quantity = item['quantity']

        if product.stock < quantity:
            messages.error(request, f"Insufficient stock for {product.name}.")
            return redirect("cart:cart_overview")
        price = product.price
        subtotal = price * quantity
        order_total += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'price': price,
            'subtotal': subtotal,
        })

        print(cart_items)

    with transaction.atomic():
        order = Order.objects.create(
            user=user,
            address=address,
            order_total=order_total,
            is_paid=False,
            status=Order.OrderStatus.PENDING,
        )

        order_items = []

        for item in cart_items:
            order_items.append(
                OrderItem(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                    price=item["price"],
                )
            )

        OrderItem.objects.bulk_create(order_items)

        # Reduce stock.
        for item in cart_items:
            product = Product.objects.select_for_update().get(pk=item["product"].pk)
            product.stock -= item['quantity']
            product.save()

        # Cash on delivery.
        if payment_method == 'COD':
            order.status = Order.OrderStatus.CONFIRMED
            order.save(update_fields=["status"])

        # Online payment
        elif payment_method == "RAZORPAY":

        # Payment will confirm later
            pass

    return order