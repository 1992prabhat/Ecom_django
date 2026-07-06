from . import views
from django.urls import path

app_name = 'users'
urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
# 	path('logout/', views.logout, name='logout'),
# 	path('profile/', views.profile, name='profile'),
]