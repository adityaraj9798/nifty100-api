from django.urls import path
from . import views

urlpatterns = [
    # Add this line for the registration endpoint
    path('register/', views.register_business, name='register'),
    
    # Your existing routes
    path('companies/', views.get_companies),
    path('companies/<str:symbol>/intelligence/', views.get_company_intelligence),
    path('companies/<str:symbol>/', views.get_company_detail),
]