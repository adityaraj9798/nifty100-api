from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.get_companies),
    path('companies/<str:symbol>/intelligence/', views.get_company_intelligence), # Specific route first!
    path('companies/<str:symbol>/', views.get_company_detail),
]