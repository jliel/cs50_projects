from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.core.exceptions import ValidationError
from django.conf import settings

class User(AbstractUser):
    pass


class Category(models.Model):
    title = models.CharField(max_length=50, blank=False)
    
    def __str__(self):
        return self.title


class AuctionListing(models.Model):
    title = models.CharField(max_length=120, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    start_bid = models.FloatField(blank=False)
    current_bid = models.FloatField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    image = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", null=True, blank=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.current_bid:
            self.current_bid = self.start_bid
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title





class Bids(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quantity = models.FloatField(blank=False, null=False)    
    bids = models.ForeignKey(AuctionListing, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Bid for {self.bids} of {self.quantity}"


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=200, blank=False, null=False)
    article = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Comment on {self.article} post"
    
