from django.urls import path

from . import views

urlpatterns = [
    path('calculators/bmi/', views.bmi_calculator, name='bmi_calculator'),
    path('calculators/tdee/', views.tdee_calculator, name='tdee_calculator'),
    path('calculators/macros/', views.macro_calculator, name='macro_calculator'),
]
