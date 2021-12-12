from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name ="index"),
    path('scan/', views.scan, name="scan"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup_page, name="signup"),
    path('logout/', views.logout_user, name="logout"),

    # ADMINS URLS
    path('admin_home/', views.admin_home, name="admin_home"),
    path('admin_users/', views.admin_users_dashboard, name="admin_users"),
    path('admin_user_info/<str:id>', views.admin_user_info, name="admin_user_info"),
    path('admin_user_pui/<str:id>', views.admin_user_pui, name="admin_user_pui"),
    path('admin_user_active/<str:id>', views.admin_user_active, name="admin_user_active"),
    path('admin_pui/', views.admin_pui_dashboard, name="admin_pui"),
    path('admin_about/', views.admin_about, name="admin_about"),
    path('admin_error', views.admin_error, name="admin_error"),

    # CLIENT URLS
    path('client_dashboard/', views.client_dashboard, name="client_dashboard"),
    path('client_contact/', views.client_contact, name="client_contact"),
    path('client_about/', views.client_about, name="client_about"),
    path('client_error/', views.client_error, name="client_error"),
]
