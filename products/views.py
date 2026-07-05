from django.shortcuts import render
from .models import Product
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def index(request):
	products = Product.objects.filter(active=True).filter(is_featured=True).order_by("id")[:8]
	return render(request, 'products/index.html', {'products': products})

def product_list(request):
	product_list = Product.objects.filter(active=True).order_by("id")

	paginator = Paginator(product_list, 12)

	page_number = request.GET.get("page")

	products = paginator.get_page(page_number)

	pagination_range = paginator.get_elided_page_range(
			products.number,
			on_each_side=2,
			on_ends=1,
	)

	return render(
			request,
			"products/product_list.html",
			{
					"products": products,
					"pagination_range": pagination_range,
			},
	)

def product_detail(request, slug):
	product = Product.objects.get(slug=slug)
	return render(request, 'products/product_detail.html', {'product': product})