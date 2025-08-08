from django.contrib import admin
from .models import User, Auctions, Watchlist, Bids, Comment

# Register your models here
admin.site.register(User)
admin.site.register(Auctions)
admin.site.register(Watchlist)
admin.site.register(Bids)
admin.site.register(Comment)