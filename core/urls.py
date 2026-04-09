from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path("search/", views.search_experts, name="search_experts"),
    path('pay/<int:expert_id>/', views.make_payment, name='make_payment'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('payment/<int:expert_id>/', views.payment_page, name='payment_page'),
    path('payment-success/<int:expert_id>/', views.payment_success, name='payment_success'),
    path('hire/<int:expert_id>/', views.hire_expert, name='hire_expert'),
    path('register-expert/', views.register_expert, name='register_expert'),
    path('expert-login/', views.expert_login, name='expert_login'),
]