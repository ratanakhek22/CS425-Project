from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .models import *;

# Views
def index(request):
    return redirect("login", usertype="customer")

def login_view(request, usertype):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = UserProfile.objects.filter(username=username, password=password)
        
        if len(user) != 0:
            login(request, user[0])
        else:
            return render(request, "real_estate/login.html", {
                "message": "Invalid username and/or password.",
                "user_type": usertype,
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

def logout_view(request):
    logout(request)
    return redirect("login", usertype="customer")
    
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
    user = Agent.objects.get(agentID=request.user)
    allProperties = user.allAssignedProperties.all()
    allBookings = []
    for property in allProperties:
        for booking in property.allBookings.all():
            allBookings.append(booking)
    return render(request, "real_estate/agentHome.html", {
        "userAgent": user,
        "allProperties": allProperties,
        "allBookings": allBookings,
    })

def company_view(request):
    if request.method == "POST":
        Agent.objects.get(pk=request.POST["employeePK"]).delete()
    user = request.user
    return render(request, "real_estate/companyHome.html", {
        "userCompany": Company.objects.get(companyID=user),
        "allEmployees": list(Company.objects.get(companyID=user).allAgents.all()),
    })
    
def customer_view(request):
    user = request.user.isCustomer.all()[0]
    return render(request, "real_estate/customerHome.html", {
        "userCustomer": user,
        "allProperties": [booking.propertyID for booking in user.myAppointments.all()],
    })
    
def browsing_view(request):
    return render(request, "real_estate/propertyList.html", {
        "allProperties": Property.objects.all(),
        "user_type": "customer",
    })
    
def property_list_view(request):
    if request.method == "POST":
        print("hi")
        
    if len(request.user.isCompany.all()) == 0:
        #customer user
        return render(request, "real_estate/propertyList.html", {
            "allProperties": Property.objects.all(),
            "user_type": "customer",
        })

    companyUser = request.user.isCompany.all()[0]
    allEmployees = companyUser.allAgents.all()
    allProperties = []
    for employee in allEmployees:
        for property in employee.allAssignedProperties.all():
            allProperties.append(property)
    
    #company user
    return render(request, "real_estate/propertyList.html", {
        "allProperties": allProperties,
        "user_type": "company",
    })
    
def add_property_view(request):
    if request.method == "POST":
        data = request.POST
        print(data["agent"])
        newProperty = Property(zip=data["zip_code"], state=data["state"], address=data["address"], price=data["price"], description=data["description"], agentID=Agent.objects.get(pk=data["agent"]))
        newProperty.save()
        return redirect("companyHome")
    return render(request, "real_estate/addProperty.html", {
        "allEmployees": request.user.isCompany.all()[0].allAgents.all(),
    })

def review_view(request, property):
    if request.method == "POST":
        newReview = Review(author=request.user.isCustomer.all()[0], propertyID=Property.objects.get(pk=property), comment=request.POST["review"])
        newReview.save()
        return redirect("propertyList")
    return render(request, "real_estate/review.html", {
        "propertyPK": property,
    })

def viewReviews_view(request, property):
    return render(request, "real_estate/viewReviews.html", {
        "allReviews": Property.objects.filter(pk=property).all()[0].allReviews.all(),
        "property": Property.objects.get(pk=property),
    })
    
def booking_view(request, property):
    newBooking = Booking(customerID=request.user.isCustomer.all()[0], propertyID=Property.objects.get(pk=property))
    newBooking.save()
    return redirect("customerHome")