from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name='login/login.html'), name="login"),  # Base URL for
    # kioskApp: ...../kioskApp/
    path("survey", views.survey, name = "survey"),  # URL for Survey ...../kioskApp/survey
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('display-data/', views.displayData, name='display_data'),
    path('completion-rate-data/', views.completion_rate_data, name='completion_rate_data'),
]