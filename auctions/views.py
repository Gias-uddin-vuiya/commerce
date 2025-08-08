from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import User, Auctions, Watchlist, Bids, Comment


def index(request):
    auction = Auctions.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auction,
    })



def watchlist(request):
    user_watchlist = Watchlist.objects.filter(user=request.user)
    auctions = [item.auction for item in user_watchlist]
   
    return render(request, "auctions/watchlist.html", {
        "watchlists": auctions,
        "user": request.user
    })

# it will add and remove the auction from the watchlist
def toggle_watchlist(request, auction_id):
    auction = get_object_or_404(Auctions, pk=auction_id)
    watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, auction=auction)

    if not created:
        watchlist_item.delete()
    return redirect("details", auction_id=auction.id)

# auction details view
def details(request, auction_id):
    # Fetch the auction by ID
    try:
        auction = Auctions.objects.get(id=auction_id)

    except Auctions.DoesNotExist:
        return HttpResponse("Auction not found.", status=404)

    # Check if the auction is in the user's watchlist
    in_watchlist = False
    if request.user.is_authenticated:
        in_watchlist = Watchlist.objects.filter(user=request.user, auction=auction).exists()
    
    # Handle POST request for placing a bid -----------==========
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        
        bid_amount = request.POST.get("bid")
        
        try:
            bid_amount = float(bid_amount)
        except (ValueError, TypeError):
            messages.error(request, "Invalid bid amount.")
            return redirect("details", auction_id=auction_id)

        # Get current highest bid
        current_bid = Bids.objects.filter(auction=auction).order_by('-bid_amount').first()
        min_bid = current_bid.bid_amount if current_bid else auction.starting_bid

        if bid_amount <= min_bid:
            messages.error(request, f"Your bid must be higher than the current bid (${min_bid}).")
        else:
            Bids.objects.create(user=request.user, auction=auction, bid_amount=bid_amount)
            messages.success(request, "Your bid has been placed successfully.")

        return redirect("details", auction_id=auction_id)
    
     # Get current highest bid (to show in template)
    current_bid = Bids.objects.filter(auction=auction).order_by('-bid_amount').first()
    highest_bid = current_bid.bid_amount if current_bid else None

    return render(request, "auctions/details.html", {
        "auction": auction,
        "in_watchlist": in_watchlist,
        "highest_bid": highest_bid,
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

def close_auction(request, auction_id):
    auction = get_object_or_404(Auctions, pk=auction_id)

    if request.method == "POST":
        if request.user == auction.creator and auction.is_active:
            # Find highest bid and set winner (if you have a Bids model)
            highest_bid = auction.bids_set.order_by('-bid_amount').first()
            if highest_bid:
                auction.winner = highest_bid.user
            auction.is_active = False
            auction.save()
            messages.success(request, "Auction closed successfully.")
        else:
            messages.error(request, "You cannot close this auction.")
    return redirect("details", auction_id=auction.id)


# comment functionality
def add_comment(request, auction_id):
    if request.method == "POST":
        content = request.POST.get("content")
        auction = get_object_or_404(Auctions, pk=auction_id)

        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to comment.")
            return redirect("login")

        if content:
            Comment.objects.create(auction=auction, user=request.user, content=content)
            messages.success(request, "Comment added successfully.")
        else:
            messages.error(request, "Comment cannot be empty.")

    return redirect("details", auction_id=auction_id)


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
