from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    
    def __str__(self):
        return self.username

class Auctions(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=512, blank=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=64, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctions")
    created_at = models.DateTimeField(auto_now_add=True)

    # NEW FIELDS
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="won_auctions")

    def __str__(self):
        return self.title
      
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="watchlist_items")
    
    def __str__(self):
        return f"{self.user.username} - {self.auction.title}"


class Bids(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.auction.title} - ${self.bid_amount}"
    
class Comment(models.Model):
    auction = models.ForeignKey(Auctions, on_delete=models.CASCADE, related_name="comments"),
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments"),
    content = models.TextField(max_length=520)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.auction.title} - {self.content[:20]}..."