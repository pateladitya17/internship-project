from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    blood_group = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username
    
class Stock(models.Model):
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=None)  # Manually added user_profile field with a default value of None

    def __str__(self):
        return self.bloodgroup

class BloodRequest(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    patient_name=models.CharField(max_length=30)
    patient_age=models.PositiveIntegerField()
    reason=models.CharField(max_length=500)
    bloodgroup=models.CharField(max_length=10)
    unit=models.PositiveIntegerField(default=0)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now=True)
    def __str__(self):
        return self.bloodgroup

class BloodDonate(models.Model): 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)   
    disease = models.CharField(max_length=100, default="Nothing")
    age = models.PositiveIntegerField()
    bloodgroup = models.CharField(max_length=10)
    unit = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default="Pending")
    date = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.user.username} - {self.bloodgroup} Donation"

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


