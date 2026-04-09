from django.db import models
from django.contrib.auth.models import User

class Expert(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    skill = models.TextField()
    skill_type = models.CharField(max_length=100, default="custom")
    solution = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username
    
class Hire(models.Model):
    user_name = models.CharField(max_length=100)
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    problem = models.TextField()
    status = models.CharField(max_length=50, default="Pending")
    payment_status = models.CharField(max_length=50, default="Not Paid")
