from .models import AuctionListing


def watchlist_processor(request):
    try:
        watchlist_count = AuctionListing.objects.filter(watchlist=request.user).count()
        print(watchlist_count)   
    except:
        watchlist_count = ""       
    return {'watch_count': watchlist_count}