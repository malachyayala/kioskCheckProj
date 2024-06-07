from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import charging_station_view, display_charging_station_data

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),  # Base URL for
    # kioskApp: ...../kioskApp/
    path("survey", views.survey, name = "survey"),  # URL for Survey ...../kioskApp/survey
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('display-data/', views.display_data, name='display_data'),
    path('completion-rate-data/', views.completion_rate_data, name='completion_rate_data'),
    path('register/', views.register, name='register'),
    path('delete/<int:pk>/', views.delete_kiosk_check, name='delete_kiosk_check'),
    path('export-data/', views.export_data, name='export_data'),
    path('charging_station/', charging_station_view, name='charging_station'),
    path('display_charging_station_data/', display_charging_station_data, name='display_charging_station_data'),
    path('delete_charging_station_check/<int:pk>/', views.delete_charging_station_check,
         name='delete_charging_station_check'),
]