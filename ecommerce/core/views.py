from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required

from .forms import CriarUsuarioForm, LoginForm
from .models import Carrinho, Categoria, Produto, ProdutoCarrinho

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
            Carrinho.objects.create(user=user)
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
            django_login(request, user)
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
    return render(request, 'lista_categoria.html', {
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
    id = request.POST['produto_id']
    produto = get_object_or_404(Produto, pk=int(id))
    carrinho = request.user.carrinho
    try:
        produto_carrinho = ProdutoCarrinho.objects.get(carrinho=carrinho, produto=produto)
        produto_carrinho.quantidade = produto_carrinho.quantidade + 1
        produto_carrinho.save()
    except ProdutoCarrinho.DoesNotExist:
        ProdutoCarrinho.objects.create(
            carrinho=carrinho,
            produto=produto
        )
    return redirect('/carrinho')


@login_required
def remover_produto_carrinho(request):
    id = request.POST['produto_id']
    produto = get_object_or_404(Produto, pk=int(id))
    carrinho = request.user.carrinho
    try:
        produto_carrinho = ProdutoCarrinho.objects.get(carrinho=carrinho, produto=produto)
        produto_carrinho.quantidade = produto_carrinho.quantidade - 1
        if produto_carrinho.quantidade <= 0:
            produto_carrinho.delete()
        else:
            produto_carrinho.save()
    except ProdutoCarrinho.DoesNotExist:
        ProdutoCarrinho.objects.create(
            carrinho=carrinho,
            produto=produto
        )
    return redirect('/carrinho')


@login_required
def carrinho(request):
    produtos_carrinho = request.user.carrinho.produtos.all()
    categorias = Categoria.objects.all()
    return render(request, 'carrinho.html', {'produtos_carrinho': produtos_carrinho, 'categorias': categorias})

@login_required
def logout(request):
    django_logout(request)
    return redirect('/home')