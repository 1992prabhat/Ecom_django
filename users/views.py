from .forms import LoginForm
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm

# Create your views here.
def register(request):
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('users:login')
	else:
		form = RegisterForm()
	return render(request, 'users/register.html', {'form': form})

def login(request):
	if request.method == 'POST':
		form = LoginForm(request, data=request.POST)
		if form.is_valid():
			form.login()
			return redirect('products:index')
	else:
		form = LoginForm()
	return render(request, 'users/login.html', {'form': form})
