from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Auctions


def index(request):
    auction = Auctions.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auction,
    })


def watchlist(request):
    # Assuming you have a Watchlist model or similar logic to fetch watchlist items
    # For now, we will just return a placeholder response
    return render(request, "auctions/watchlist.html", {
        "message": "Your Watchlist"
    })

def details(request, auction_id):
    try:
        auction = Auctions.objects.get(id=auction_id)
       
    except Auctions.DoesNotExist:
        return HttpResponse("Auction not found.", status=404)

    return render(request, "auctions/details.html", {
        "auction": auction,
        "message": "Auction Details"
    })

def create(request):

    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image_url = request.POST.get("image_url", "")
        category = request.POST.get("category", "")

        # Create a new auction
        auction = Auctions(
            title=title,
            description=description,
            starting_bid=starting_bid,
            image_url=image_url,
            category=category,
            creator=request.user
        )
        # Save the auction to the database
        auction.save()
        
        if auction.id:
            return HttpResponseRedirect(reverse("index"), {
                "message": "Auction created successfully!"})
        # Redirect to the index page after creating the auction 
        else:
           return render(request, "auctions/create.html", {
                "message": "Error creating auction. Please try again."
            })

    return render(request, "auctions/create.html", {
        "message": "Create Auction"
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
