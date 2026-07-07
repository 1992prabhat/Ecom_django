from . import views
from django.urls import path

app_name = 'users'
urlpatterns = [
	path('register/', views.register, name='register'),
	path('login/', views.login, name='login'),
	path('logout/', views.logout, name='logout'),
	path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email_verification'),
	path('email-verification_sent/', views.email_verification_sent, name='email_verification_sent'),
	path('email-verification-success/', views.email_verification_success, name='email_verification_success'),
	path('email-verification-failed/', views.email_verification_failed, name='email_verification_failed'),
	path('profile/', views.profile, name='profile'),
	path('change-password/', views.change_password, name='change_password'),
]