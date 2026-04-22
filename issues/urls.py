from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('report/', views.report_issue, name='report_issue'),
    path('issues/', views.issues_list, name='issues_list'),
    path('map/', views.map_view, name='map_view'),
    path('api/map-data/', views.map_data, name='map_data'),
    path('issue/<int:pk>/', views.issue_detail, name='issue_detail'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('official/', views.official_dashboard, name='official_dashboard'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]
