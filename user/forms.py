from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "large-input", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "large-input", "placeholder": "Repeat Password"}),
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            "username": forms.TextInput(attrs={"class": "large-input", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "large-input", "placeholder": "Email Address"}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash password
        if commit:
            user.save()
        return user
