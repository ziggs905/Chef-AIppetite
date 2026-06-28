from django.urls import path

from . import views

urlpatterns = [
    path('mealplans/', views.plan_list, name='plan_list'),
    path('mealplans/new/', views.plan_create, name='plan_create'),
    path('mealplans/<int:pk>/', views.plan_detail, name='plan_detail'),
    path('mealplans/<int:pk>/delete/', views.plan_delete, name='plan_delete'),
    path('mealplans/<int:pk>/entries/<int:entry_pk>/swap/', views.plan_entry_swap, name='plan_entry_swap'),
    path(
        'mealplans/<int:pk>/entries/<int:entry_pk>/toggle-completed/',
        views.plan_entry_toggle_completed,
        name='plan_entry_toggle_completed',
    ),
    path(
        'mealplans/<int:pk>/generate/<str:meal_slot>/',
        views.plan_generate_slot_recipe,
        name='plan_generate_slot_recipe',
    ),
    path(
        'mealplans/<int:pk>/days/<int:day>/<str:meal_slot>/fill/',
        views.plan_fill_entry,
        name='plan_fill_entry',
    ),
]
