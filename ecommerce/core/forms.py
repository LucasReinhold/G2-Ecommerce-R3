from django import forms

from django.contrib.auth.models import User


class CriarUsuarioForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    primeiro_nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    senha = forms.CharField(max_length=30)

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username']).exists():
            raise forms.ValidationError('Username já existe.', code='invalid')
        return self.cleaned_data['username']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    senha = forms.CharField(max_length=30)
