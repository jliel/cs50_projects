from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Bids, Comment, Category

from .forms import NewListingForm


def index(request):
    listing = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {"listing": listing})


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


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            listing = AuctionListing(
                title=cd["title"],
                description=cd["description"],
                start_bid=cd["start_bid"],
                category=cd["category"],
                image=cd["image"],
                user=request.user
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = NewListingForm()
    return render(request, "auctions/new.html", {"form": form})


@login_required(login_url='/login')
def listing_detail(request, id):
    bids_count = ""
    higest = None
    winner = None
    comments = None
    listing= None
    error_mesage = None
    try:
        listing = AuctionListing.objects.get(id=id)
        try:
            bids_count = Bids.objects.filter(bids=listing.id).count()
            higest = Bids.objects.filter(bids=listing).latest('created')
            comments = Comment.objects.filter(article=listing).order_by("-created")
        except:
            pass
        try:
            comments = Comment.objects.filter(article=listing).order_by("-created")
        except:
            comments = None
        if not listing.active:
            winner = listing.winner
    except:
        error_mesage = "404 Page not found"
    return render(request, "auctions/detail.html", {
        "listing": listing,
        "bids_count": bids_count,
        "bid_data": higest,
        "winner": winner,
        "comments": comments,
        "error": error_mesage
    })


@login_required(login_url='/login')
def bid(request, id):
    listing = AuctionListing.objects.get(id=id)
    if request.method == "POST":
        bid = request.POST["bid"]
        if float(bid) > listing.current_bid:
            new_bid = Bids(quantity=float(
                bid), bids=listing, user=request.user)
            listing.current_bid = new_bid.quantity
            new_bid.save()
            listing.save()
    return listing_detail(request, id)


@login_required(login_url='/login')
def close_listing(request, id):
    listing = AuctionListing.objects.get(id=id)
    listing.active = False
    try:
        higest_bid = Bids.objects.filter(bids=listing).latest('created')
        winner = higest_bid.user
    except:
        winner = None
    listing.winner = winner
    listing.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url="/login")
def add_comment(request, id):
    listing = AuctionListing.objects.get(id=id)
    if request.method == "POST":
        comment = Comment(content=request.POST["content"])
        comment.user = request.user
        comment.article = listing
        comment.save()
    return listing_detail(request, listing.id)


def list_categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


def filter_categories(request, category):
    listing = AuctionListing.objects.filter(category=category)
    filter_category = True
    return render(request, "auctions/index.html", {"listing": listing, "filter": filter_category})


@login_required(login_url="/login")
def watch_listing(request, username):
    listing =  AuctionListing.objects.filter(watchlist=request.user)
    watchlist = True
    return render(request, "auctions/index.html", {"listing": listing, "watchlist": watchlist})


@login_required(login_url="/login")
def add_watch_list(request, id):
    listing = AuctionListing.objects.get(id=id)
    listing.watchlist.add(request.user)
    print("saving")
    listing.save()
    return listing_detail(request, listing.id)