from django.db import models

# Create your models here.
# class Cart(models.Model):
# 		# Define the fields for the Cart model
# 		# For example, you might want to store the user associated with the cart
# 		user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
# 		created_at = models.DateTimeField(auto_now_add=True)
# 		updated_at = models.DateTimeField(auto_now=True)

# 		def __str__(self):
# 				return f"Cart for {self.user.username} (ID: {self.id})"

# class CartItem(models.Model):
# 		cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
# 		product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
# 		quantity = models.PositiveIntegerField(default=1)

# 		def __str__(self):
# 				return f"{self.quantity} x {self.product.name} in Cart ID: {self.cart.id}"