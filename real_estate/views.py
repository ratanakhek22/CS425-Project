from django.shortcuts import render

# Views
def login_view(request):
    if request.method == "POST":
        # check for customer type and display different pages
        if request.POST["user_type"] == "customer":
            return render(request, "real_estate/customerHome.html")
        elif request.POST["user_type"] == "agent":
            return render(request, "real_estate/agentHome.html")
        elif request.POST["user_type"] == "company":
            return render(request, "real_estate/companyHome.html")
    else:
        return render(request, "real_estate/login.html")
    
def register_view(request):
    if request.method == "POST":
        # try to register the user if can't render register again
        return render(request, "real_estate/login.html")
    else:
        return render(request, "real_estate/register.html")