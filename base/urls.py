from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ="index"),
    path('scan/', views.scan, name="scan"),
    path('login/', views.login_signup, name="login"),

    # ADMINS URLS
    path('admin_home/', views.admin_home, name="login"),
    path('admin_users/', views.admin_users_dashboard, name="admin_users"),
    path('admin_user_info/', views.admin_user_info, name="admin_user_info"),
    path('admin_pui/', views.admin_pui_dashboard, name="admin_pui"),
    path('admin_about/', views.admin_about, name="admin_about"),

    # CLIENT URLS
    path('client_dashboard/', views.client_dashboard, name="client_dashboard"),
    path('client_contact/', views.client_contact, name="client_contact"),
    path('client_about/', views.client_about, name="client_about"),
]
