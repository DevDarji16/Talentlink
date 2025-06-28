from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES=[('client','Client'),('freelancer','Freelancer'),('both','Both')]

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    role=models.CharField(max_length=20,choices=ROLE_CHOICES)
    username=models.CharField(max_length=20,unique=True)
    fullname=models.CharField(max_length=200)
    profilepic=models.URLField(max_length=500,blank=True,default='https://res.cloudinary.com/dmebvno0m/image/upload/v1749882603/veilzulxlqv2tjk1ncgs.jpg')

    description=models.TextField(blank=True,default="")

    #freelancer
    skills=models.JSONField(blank=True,null=True)
    experience=models.IntegerField(blank=True,null=True)
    portfolio_link=models.URLField(blank=True,null=True)
    hourly_rate=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    #client thing
    company_name= models.CharField(max_length=100,blank=True,null=True)
    company_site= models.URLField(blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username
