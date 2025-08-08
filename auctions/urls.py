from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("close_auction/<int:auction_id>", views.close_auction, name="close_auction"),
    path("details/<int:auction_id>", views.details, name="details"),
    path("details/<int:auction_id>/toggle_watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("details/<int:auction_id>/add_comment", views.add_comment, name="add_comment"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
