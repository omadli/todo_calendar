import email
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from accounts.models import User


class SignInForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "input100", "placeholder": "Email"}))  # noqa: E501
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Password"})  # noqa: E501
    )


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Password"}),
        validators=[validate_password],
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "input100", "placeholder": "Confirm password"}),
        validators=[validate_password],
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input100", "required": "true", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "input100", "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": "input100", "placeholder": "Email"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        exist_email = User.objects.filter(email=email).exists()
        if exist_email:
            raise ValidationError("This email already registered")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password didn't match!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
