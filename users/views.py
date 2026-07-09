from .forms import LoginForm
from django.shortcuts import render, redirect, reverse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.template.loader import render_to_string
from .token import account_activation_token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .decorators import anonymous_required
from .forms import ProfileForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .mixins import AnonymousRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomPasswordResetForm, CustomSetPasswordForm
from django.urls import reverse_lazy
from .models import Address
from .forms import AddressForm

# Create your views here.
# Only anonymous users can visit this view
@anonymous_required
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            # Email verification logic
            subject = "Verify your email to activate your account."

            verification_url = request.build_absolute_uri(
                        reverse(
                                "users:email_verification",
                                kwargs={
                                        "uidb64": urlsafe_base64_encode(force_bytes(user.pk)),
                                        "token": account_activation_token.make_token(user),
                                },
                        )
                )

            message = render_to_string('users/email_verification.html',
                                                            {
                                                                'user': user,
                                                                'verification_url': verification_url,
                                                                })

            email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,
                    to=[user.email],
            )

            email.attach_alternative(message, "text/html")
            email.send()
            # user.email_user(subject, message)

            return redirect('users:email_verification_sent')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

@anonymous_required
def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('products:index')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('products:index')

def email_verification(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)
    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('users:email_verification_success')
    else:
        return redirect('users:email_verification_failed')

def email_verification_sent(request):
    return render(request, 'users/email_verification_sent.html')

def email_verification_success(request):
    return render(request, 'users/email_verification_success.html')

def email_verification_failed(request):
    return render(request, 'users/email_verification_failed.html')

@login_required
def profile(request):
    form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)

    addresses = Address.objects.filter(user=request.user).order_by('-default', '-id')[:2]

    return render(
        request,
        "users/profile.html",
        {
                "form": form,
                "addresses": addresses,
        },
    )

@login_required
def change_password(request):
        form = ChangePasswordForm(request.user)
        if request.method == 'POST':
                form = ChangePasswordForm(request.POST, request.user)
                if form.is_valid():
                        user = form.save()
                        update_session_auth_hash(request, user)
                        return redirect('users:profile')
        else:
                return render(request, 'users/change_password.html', {'form': form})


# Reset Password views.
class CustomPasswordResetView(AnonymousRequiredMixin, PasswordResetView):
    template_name = "users/password_reset.html"
    form_class = CustomPasswordResetForm
    email_template_name = "users/password_reset_email.html"
    success_url = reverse_lazy("users:password_reset_done")

class CustomPasswordResetDoneView(AnonymousRequiredMixin, PasswordResetDoneView):
    template_name = "users/password_reset_done.html"
    success_url = reverse_lazy("users:password_reset_complete")

class CustomPasswordResetConfirmView(AnonymousRequiredMixin, PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy("users:password_reset_complete")

class CustomPasswordResetCompleteView(AnonymousRequiredMixin, PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"
    success_url = reverse_lazy("users:login")


#Address views.
@login_required
def add_address(request):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user

            if not Address.objects.filter(user=request.user, default=True).exists():
                address.default = True

            address.save()
            return redirect("users:profile")

        else:
            form = AddressForm()

    return render(
        request,
        "users/add_address.html",
        {"form": form},
    )

@login_required
def edit_address(request, pk):
    address = Address.objects.get(pk=pk)
    if address.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this address.")

    form = AddressForm(instance=address)
    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            if not Address.objects.filter(user=request.user, default=True).exclude(pk=address.pk).exists():
                address.default = True
            address.save()
            return redirect("users:profile")
        else:
            form = AddressForm(instance=address)
    return render(
        request,
        "users/add_address.html",
        {"form": form},
    )

@login_required
def delete_address(request, pk):
    address = Address.objects.get(pk=pk)
    if address.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this address.")
    address.delete()
    return redirect("users:profile")

def address_list(request):
    addresses = Address.objects.filter(user=request.user).order_by('-default', '-id')
    return render(request, 'users/address_list.html', {'addresses': addresses})

def set_default_address(request, pk):
    address = Address.objects.get(pk=pk)
    if address.user != request.user:
        return HttpResponseForbidden("You don't have permission to set this address as default.")
    address.default = True
    address.save()

    # Set other addresses as non-default.
    Address.objects.filter(user=request.user, default=True).exclude(pk=address.pk).update(default=False)
    return redirect("users:address_list")
