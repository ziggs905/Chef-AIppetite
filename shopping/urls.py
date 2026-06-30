from django.urls import path

from . import views

urlpatterns = [
    path('shopping/', views.shopping_list_index, name='shopping_list_index'),
    path('shopping/generate/<int:plan_pk>/', views.shopping_list_generate, name='shopping_list_generate'),
    path('shopping/<int:pk>/', views.shopping_list_detail, name='shopping_list_detail'),
    path('shopping/<int:pk>/delete/', views.shopping_list_delete, name='shopping_list_delete'),
    path('shopping/<int:pk>/items/<int:item_pk>/edit/', views.shopping_item_edit, name='shopping_item_edit'),
    path('shopping/<int:pk>/items/<int:item_pk>/delete/', views.shopping_item_delete, name='shopping_item_delete'),
    path('shopping/<int:pk>/items/<int:item_pk>/toggle/', views.shopping_item_toggle, name='shopping_item_toggle'),
]
