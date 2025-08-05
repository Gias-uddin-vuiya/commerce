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

    def __str__(self):
        return self.title
      