from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserProfile(AbstractUser, models.Model):
    password = models.CharField(max_length=20)
    username = models.CharField(max_length=30, unique=True)
    
class Company(models.Model):
    name = models.CharField(max_length=30)
    companyID = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="isCompany")
    
    def _str_(self):
        return self.name
    
class Agent(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    agentID = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="isAgent")
    companyID = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="allAgents")
    
class Customer(models.Model):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=10)
    customerID = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="isCutomer")

class Property(models.Model):
    zip = models.IntegerField()
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=30)
    price = models.IntegerField()
    desciption = models.TextField()
    ownerName = models.CharField(max_length=30)
    agentID = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="allAssignedProperties")
    
class Review(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="myReviews")
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="allReviews")
    date = models.DateField() # datetime.date instance (python)
    comment = models.TextField()
    
class Booking(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="myAppointments")
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="allBookings")
    date = models.DateField(auto_now_add=True)