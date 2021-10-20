"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect

from core import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', lambda _: redirect('/home')),
    path('admin/', admin.site.urls),
    path('criarusuario', views.criar_usuario),
    path('login', views.login),
    path('categoria/<int:id>', views.lista_categoria),
    path('home', views.home),
    path('produto/<int:id>', views.detalhe_produto),
    path('adicionar_produto', views.adicionar_produto_carrinho),
    path('remover_produto', views.remover_produto_carrinho),
    path('carrinho', views.carrinho),
    path('logout', views.logout),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
