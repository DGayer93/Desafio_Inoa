from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomLoginView

urlpatterns = [
    path('accounts/profile/<int:user_id>/registrarativo/', views.registrar_ativo, name='registrar_ativo'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('accounts/profile/<int:user_id>/visualizar_ativos', views.visualizar_ativos, name='visualizar'),
    path('accounts/profile/<int:user_id>/alertas/', views.alertas, name='alertas'),
    path('logout/',views.logout_view,name='logout'),
    path('accounts/profile/<int:user_id>/editar_ativo/<int:id>',views.editar_ativo,name='editar'),
    path('accounts/profile/<int:user_id>/deletar_ativo/<int:id>',views.deletar_ativo,name='deletar')
]