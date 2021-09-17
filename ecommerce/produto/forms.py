from django import forms


class CriarUsuarioForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    primeiro_nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    senha = forms.CharField(max_length=30)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    senha = forms.CharField(max_length=30)
