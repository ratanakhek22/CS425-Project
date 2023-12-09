from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    
    path("login/<str:usertype>/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    
    path("agent/", views.agent_view, name="agentHome"),
    path("company/", views.company_view, name="companyHome"),
    path("customer/", views.customer_view, name="customerHome"),
    
    path("browse/", views.browsing_view, name="browse"),
]
