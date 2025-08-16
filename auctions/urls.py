from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_listing", views.my_listing, name="my_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category_details, name="category_details"),
    path("close_auctions", views.close_auctions, name="close_auctions"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("details/<int:auction_id>", views.details, name="details"),
    path("details/<int:auction_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("details/<int:auction_id>/add_comment", views.add_comment, name="add_comment"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
