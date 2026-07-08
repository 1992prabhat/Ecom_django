from . import views
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import CustomPasswordResetForm, CustomSetPasswordForm


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
			auth_views.PasswordResetView.as_view(
					template_name='users/reset_password.html',
					form_class=CustomPasswordResetForm,
					email_template_name="users/password_reset_email.html",
					success_url=reverse_lazy("users:password_reset_done"),
			),
			name='password_reset'),

	path(
			'reset-password/done/',
			auth_views.PasswordResetDoneView.as_view(
					template_name='users/password_reset_done.html'),
					name='password_reset_done'),

	path(
			'reset-password/confirm/<uidb64>/<token>/',
			auth_views.PasswordResetConfirmView.as_view(
					template_name='users/password_reset_confirm.html',
					form_class=CustomSetPasswordForm,
					success_url=reverse_lazy("users:password_reset_complete"),
					),
			name='password_reset_confirm'),


	path(
			'reset-password/complete/',
			auth_views.PasswordResetCompleteView.as_view(
					template_name='users/password_reset_complete.html'),
			name='password_reset_complete'),
]