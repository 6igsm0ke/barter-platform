from django.db import models
from users.models import User
# Create your models here.

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Condition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE) 
    title = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=255, blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    id = models.AutoField(primary_key=True)
    ad_sender = models.ForeignKey('Ad', related_name='ad_sender', on_delete=models.CASCADE) 
    ad_receiver = models.ForeignKey('Ad', related_name='ad_receiver', on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return f"Proposal from {self.ad_sender} to {self.ad_receiver} - {self.status}" 