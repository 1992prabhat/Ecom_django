from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django import forms
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "username": "Enter username",
            "email": "Enter email address",
            "first_name": "First name",
            "last_name": "Last name",
            "password1": "Create a password",
            "password2": "Confirm your password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none",
                "placeholder": placeholders.get(name, ""),
            })

class LoginForm(AuthenticationForm):
	class Meta:
			fields = [
					"username",
					"password",
			]

	def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			for field in self.fields.values():
					field.widget.attrs.update({
							'class': 'w-full border border-gray-300 rounded-xl p-3 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none',
              'placeholder': field.label,
					})


class ProfileForm(forms.ModelForm):
		class Meta:
				model = User
				fields = ["first_name", "last_name", "email"]
				exclude = ["username", "password1", "password2"]

		def __init__(self, *args, **kwargs):
				super().__init__(*args, **kwargs)

				for field in self.fields.values():
						field.widget.attrs.update({
								"class": (
										"w-full pl-11 pr-4 py-3 rounded-xl border border-gray-300 "
										"bg-white shadow-sm transition duration-200 "
										"focus:outline-none focus:ring-2 focus:ring-blue-500 "
										"focus:border-blue-500 hover:border-blue-400"
								)
						})

from django import forms

class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            "old_password": "Enter your current password",
            "new_password1": "Enter your new password",
            "new_password2": "Confirm your new password",
        }

        for name, field in self.fields.items():
            field.widget.attrs.update({
                "class": (
                    "w-full px-4 py-3 rounded-xl border border-gray-300 "
                    "bg-white shadow-sm transition "
                    "focus:outline-none focus:ring-2 "
                    "focus:ring-blue-500 focus:border-blue-500"
                ),
                "placeholder": placeholders.get(name, ""),
            })