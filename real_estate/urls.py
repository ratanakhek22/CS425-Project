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
    
    path("propert_list/", views.property_list_view, name="propertyList"),
    path("addProperty/", views.add_property_view, name="addProperty"),
    
    path("booking/<int:property>/", views.booking_view, name="booking"),
    
    path("review/<int:property>/", views.review_view, name="review"),
    path("viewReviews/<int:property>/", views.viewReviews_view, name="viewReviews"),
]
