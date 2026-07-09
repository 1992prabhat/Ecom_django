from products.models import Product
from decimal import Decimal

class Cart():
	def __init__(self, request):
		self.session = request.session
		cart = request.session.get('cart')
		if not cart:
			cart = {}
			request.session['cart'] = cart
		self.cart = cart

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def __iter__(self):
		cart = self.cart.copy()

		product_ids = cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def add(self, product, quantity=1):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		self.cart[product_id]['quantity'] += quantity
		self.save()

	def remove(self, product_id):
		product_id = str(product_id)
		if product_id in self.cart:
			del self.cart[product_id]
		self.save()

	def update(self, product_id, quantity):
		product_id = str(product_id)
		if product_id in self.cart:
			if quantity <= 0:
				self.remove(product_id)
			else:
				self.cart[product_id]['quantity'] = quantity
		self.save()

	def save(self):
		self.session.modified = True

	def clear(self):
		self.session.pop("cart", None)
		self.save()

	def is_empty(self):
		return len(self.cart) == 0