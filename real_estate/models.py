from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(models.Model):
    userID = models.IntegerField()
    password = models.TextField()
    username = models.TextField()
    
class Company(models.Model):
    name = models.TextField
    companyID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="isCompany")
    
class Agent(models.Model):
    name = models.TextField()
    phone = models.TextField(max_length=10)
    agentID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="isAgent")
    companyID = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="allAgents")
    
class Customer(models.Model):
    name = models.TextField()
    phone = models.TextField(max_length=10)
    customerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name="isCutomer")

class Property(models.Model):
    zip = models.IntegerField()
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=30)
    price = models.IntegerField()
    desciption = models.TextField()
    ownerName = models.TextField()
    propertyID = models.IntegerField()
    agentID = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="allAssignedProperties")
    
class Review(models.Model):
    author = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="myReviews")
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="allReviews")
    date = models.DateField() # datetime.date instance (python)
    comment = models.TextField()
    
class Booking(models.Model):
    customerID = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="myAppointments")
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="allBookings")
    date = models.DateField() # datetime.date instance (python)