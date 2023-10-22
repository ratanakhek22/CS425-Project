from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    user_type = models.CharField(max_length=8) # Agent/Customer/Company

class Post(models.Model):
    post_type = models.CharField(max_length=10) # commercial/house/apartment
    zip = models.IntegerField()
    state = models.CharField(max_length=2)
    address = models.CharField(max_length=30)
    price = models.IntegerField()
    desciption = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allPosts")
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="allComments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allReviews")
    date = models.DateField() # datetime.date instance (python)
    comment = models.TextField()
    
class Booking(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allJobs")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allBookings")
    date = models.DateField() # datetime.date instance (python)