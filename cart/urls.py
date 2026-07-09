from django.urls import path
from . import views
app_name = 'cart'
urlpatterns = [
	# path('', views.cart, name='cart'),
	path('add/', views.cart_add, name='cart_add'),
	path('update/', views.update_cart, name='update_cart'),
	path('remove/', views.remove_from_cart, name='remove_from_cart'),
	path('overview/', views.cart_overview, name='cart_overview'),
	path('checkout/', views.checkout, name='checkout'),

]