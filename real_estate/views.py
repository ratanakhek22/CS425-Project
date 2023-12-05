from django.shortcuts import render, redirect
from .models import *;

# Views
def index(request):
    return redirect(login_view, usertype="customer")

def login_view(request, usertype):
    if request.method == "POST":
        # check for customer type and display different pages
        if request.POST["user_type"] == "customer":
            return render(request, "real_estate/customerHome.html")
        elif request.POST["user_type"] == "agent":
            return render(request, "real_estate/agentHome.html")
        elif request.POST["user_type"] == "company":
            return render(request, "real_estate/companyHome.html")
    else:
        return render(request, "real_estate/login.html", {
            "user_type": usertype,
        })
    
def register_view(request, usertype):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        if username in UserProfile.objects.values_list('username', flat=True):
            return render(request, "real_estate/register.html", {
                "message": "Username already taken."
            })
        else:
            user = UserProfile(username=username, password=password)
            user.save()
            
            if usertype == "customer":
                cust = Customer(name=request.POST["name"], phone=request.POST["phone"], customerID=user)
                cust.save()
            if usertype == "agent":
                agent = Agent(name=request.POST["name"], phone=request.POST["phone"], agentID=user)
                agent.save()
            elif usertype == "company":
                comp = Company(name=request.POST["name"], companyID=user)
                comp.save()
        
        return render(request, "real_estate/login.html", {
            "user_type": usertype,
        })
    else:
        return render(request, "real_estate/register.html", {
            "user_type": usertype,
            "allCompanies": [] if usertype != "agent" else Company.objects.all(),
        })
        
def agent_view(request):
    return render(request, "real_estate/agentHome.html", {
        "allAgents": Agent.objects.all(),
    })