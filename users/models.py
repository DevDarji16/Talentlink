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

    work_experience = models.JSONField(blank=True, null=True)
    languages = models.JSONField(blank=True, null=True)
    projects = models.JSONField(blank=True, null=True)

    leader_of = models.JSONField(default=list)  

    skills=models.JSONField(blank=True,null=True)
    experience=models.IntegerField(blank=True,null=True)
    portfolio_link=models.URLField(blank=True,null=True)
    hourly_rate=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

    company_name= models.CharField(max_length=100,blank=True,null=True)
    company_site= models.URLField(blank=True,null=True)

    wallet_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

class Gig(models.Model):
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='gigs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.JSONField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    images = models.JSONField(blank=True, null=True)  # list of image URLs
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # NEW field
    def __str__(self):
        return self.title


class Job(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    tags = models.JSONField(blank=True, null=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('hired', 'Hired'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.title


class FreelanceGroup(models.Model):
    name=models.CharField(max_length=100)
    leader = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='led_groups')
    description = models.TextField(blank=True)
    skills = models.JSONField(default=list)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    members = models.ManyToManyField(UserProfile, related_name='groups', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='applications')
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_applications')
    group = models.ForeignKey(FreelanceGroup, on_delete=models.CASCADE, null=True, blank=True)
    proposal_text = models.TextField()
    expected_timeline = models.CharField(max_length=255)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_group = models.BooleanField(default=False)
    is_individual = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.freelancer.username} → {self.job.title}'




class GroupInvite(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    
    sender = models.ForeignKey('UserProfile',on_delete=models.CASCADE,related_name='sent_group_invites')
    receiver = models.ForeignKey('UserProfile',on_delete=models.CASCADE,related_name='received_group_invites')
    group = models.ForeignKey('FreelanceGroup',on_delete=models.CASCADE,related_name='group_invites')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite from {self.sender.username} to {self.receiver.username} for {self.group.name}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('group_invite', 'Group Invite'),
        ('group_update', 'Group Update'),
    ]

    user = models.ForeignKey( 'UserProfile', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_group = models.ForeignKey('FreelanceGroup',on_delete=models.SET_NULL,null=True,blank=True)
    related_invite = models.ForeignKey('GroupInvite',on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.type}"


