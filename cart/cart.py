from products.models import Product

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
				product_ids = self.cart.keys()
				products = Product.objects.filter(id__in=product_ids)
				for product in products:
						self.cart[str(product.id)]['product'] = product

				for item in self.cart.values():
						item['price'] = float(item['price'])
						item['total_price'] = float(item['price']) * item['quantity']
						yield item

		def get_total_price(self):
				return sum(float(item['price']) * item['quantity'] for item in self.cart.values())

		def add(self, product, quantity=1):
				product_id = str(product.id)
				if product_id not in self.cart:
						self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
				self.cart[product_id]['quantity'] += quantity
				self.session.modified = True

		def remove(self, product_id):
				product_id = str(product_id)
				if product_id in self.cart:
						del self.cart[product_id]
				self.session.modified = True

		def update(self, product_id, quantity):
				product_id = str(product_id)
				if product_id in self.cart:
						self.cart[product_id]['quantity'] = quantity
				self.session.modified = True