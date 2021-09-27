from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .forms import CriarUsuarioForm, LoginForm
from .models import Categoria, Produto

def criar_usuario(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        form = CriarUsuarioForm(request.POST)
        if form.is_valid():
            user = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['primeiro_nome'],
                last_name=form.cleaned_data['sobrenome'],
            )
            user.set_password(form.cleaned_data['senha'])
            user.save()
            return redirect('/login')
    else:
        form = CriarUsuarioForm()

    return render(request, 'criar_usuario.html', {'form': form, 'categorias': categorias})


def login(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['senha']
            )
            login(request, user)
            return redirect('/home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'categorias': categorias})


def home(request):
    categorias = Categoria.objects.all()
    produtos = Produto.objects.all().order_by('-quantidade_estoque')[:10]
    return render(request, 'home.html', {'categorias': categorias, 'produtos': produtos})


def lista_categoria(request, id):
    categorias = Categoria.objects.all()
    categoria = get_object_or_404(Categoria, pk=id)
    pagina = request.GET.get('pagina', 1)
    produtos = categoria.produtos.all()[(pagina - 1) * 12: pagina * 12]
    return render(request, 'list_categoria.html', {
        'categorias': categorias,
        'categoria': categoria,
        'produtos': produtos
    })


def detalhe_produto(request, id):
    categorias = Categoria.objects.all()
    produto = get_object_or_404(Produto, pk=id)
    return render(request, 'detalhe_produto.html', {'categorias': categorias, 'produto': produto})


@login_required
def adicionar_produto_carrinho(request):
    pass


@login_required
def remover_produto_carrinho(request):
    pass


@login_required
def carrinho(request):
    pass
