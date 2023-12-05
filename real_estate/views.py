from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *;

# Views
def index(request):
    return redirect("login", usertype="customer")

def login_view(request, usertype):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = UserProfile.objects.get(username=username, password=password)
        
        print([user.username, user.password, user.pk] if user is not None else "none")
        
        if user is not None:
            login(request, user)
        else:
            return render(request, "real_estate/login.html", {
                "message": "Invalid username and/or password."
            })
        
        # check for customer type and display different pages
        if usertype == "customer":
            return redirect("customerHome")
        elif usertype == "agent":
            return redirect("agentHome")
        elif usertype == "company":
            return redirect("companyHome")
    else:
        return render(request, "real_estate/login.html", {
            "user_type": usertype,
        })
    
def register_view(request):
    if request.method == "POST" and request.POST["operation"] != "getRegPage":
        username = request.POST["username"]
        password = request.POST["password"]
        
        if username in UserProfile.objects.values_list('username', flat=True):
            return render(request, "real_estate/register.html", {
                "message": "Username already taken."
            })
        else:
            user = UserProfile(username=username, password=password)
            user.save()
            
            if request.POST["usertype"] == "customer":
                cust = Customer(name=request.POST["name"], phone=request.POST["phone"], customerID=user)
                cust.save()
            elif request.POST["usertype"] == "agent":
                agent = Agent(name=request.POST["name"], phone=request.POST["phone"], agentID=user, companyID=Company.objects.get(pk=request.POST["company"]))
                agent.save()
            elif request.POST["usertype"] == "company":
                comp = Company(name=request.POST["name"], companyID=user)
                comp.save()
        
        return render(request, "real_estate/login.html", {
            "user_type": request.POST["usertype"],
        })
    else:
        return render(request, "real_estate/register.html", {
            "user_type": request.POST["usertype"],
            "allCompanies": [] if request.POST["usertype"] != "agent" else Company.objects.all(),
        })

def agent_view(request):
    user = request.user.isAgent
    return render(request, "real_estate/agentHome.html", {
        "userAgent": user,
    })

def company_view(request):
    user = request.user
    return render(request, "real_estate/companyHome.html", {
        "userCompany": Company.objects.get(companyID=user),
        "allEmployees": Company.objects.get(companyID=user).allAgents.all()
    })
    
def customer_view(request):
    user = request.user
    return render(request, "real_estate/customerHome.html", {
        "userCustomer": Customer.objects.get(customerID=user),
    })