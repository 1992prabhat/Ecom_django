from products.models import Product
from decimal import Decimal
from .models import Cart as CartModel, CartItem
from django.db.models import Sum

class Cart():
	def __init__(self, request):
		self.request = request
		self.user = request.user

		self.cart, _ = CartModel.objects.get_or_create(user=self.user)

	def __len__(self):
		return (self.cart.items.aggregate(total = Sum('quantity'))["total"] or 0)

	def __iter__(self):
		items = self.cart.items.select_related('product')

		for item in items:
			yield {
				'product': item.product,
				'quantity': item.quantity,
				'price': item.product.price,
				'total_price': item.total_price,
			}

	def get_total_price(self):
		total = Decimal('0.00')

		for item in self.cart.items.select_related('product'):
			total += item.total_price

		return total

	def add(self, product, quantity=1):
		item, created = CartItem.objects.get_or_create(cart = self.cart, product = product)

		if created:
			item.quantity = quantity
		else:
			item.quantity += quantity
		item.save()

	def remove(self, product_id):
		cart_item = CartItem.objects.filter(cart = self.cart, product = product_id)
		if cart_item.exists():
			cart_item.delete()

	def update(self, product_id, quantity):
		try:
			item = CartItem.objects.get(cart = self.cart, product = product_id)
		except CartItem.DoesNotExist:
			return

		if quantity <= 0:
			self.remove(product_id)
		else:
			item.quantity = quantity
			item.save(update_fields=['quantity'])

	def clear(self):
		self.cart.items.all().delete()

	def is_empty(self):
		return not self.cart.items.exists()