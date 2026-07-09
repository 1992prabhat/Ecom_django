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

	# Reset Password flow.
	path(
			'reset-password/',
			views.CustomPasswordResetView.as_view(),
			name='password_reset'),

	path(
			'reset-password/done/',
			views.CustomPasswordResetDoneView.as_view(),
			name='password_reset_done'),

	path(
			'reset-password/confirm/<uidb64>/<token>/',
			views.CustomPasswordResetConfirmView.as_view(),
			name='password_reset_confirm'),


	path(
			'reset-password/complete/',
			views.CustomPasswordResetCompleteView.as_view(),
			name='password_reset_complete'),

	#Address views
	path('add-address/', views.add_address, name='add_address'),
	path('edit-address/<int:pk>/', views.edit_address, name='edit_address'),
	path('delete-address/<int:pk>/', views.delete_address, name='delete_address'),
	path('address-list/', views.address_list, name='address_list'),
	path('set-default-address/<int:pk>/', views.set_default_address, name='set_default_address'),
]