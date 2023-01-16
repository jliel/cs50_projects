from django.contrib import admin

from .models import Category, AuctionListing, Bids, Comment, User


admin.site.register(Category)
admin.site.register(AuctionListing)
admin.site.register(Bids)
admin.site.register(Comment)
admin.site.register(User)