from django import forms

class CreateUserForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.PasswordInput()