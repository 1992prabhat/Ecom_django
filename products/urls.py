from django.urls import path
from . import views
app_name = 'products'
urlpatterns = [
	path('', views.index, name='index'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),
]