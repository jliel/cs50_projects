from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories/", views.list_categories, name="list_categories"),
    path("<int:category>/", views.filter_categories, name="filter_categories"),
    path("listing/new/", views.new_listing, name="new_listing"),
    path("listing/<int:id>/", views.listing_detail, name="listing"),
    path("listing/<int:id>/bid/", views.bid, name="bid"),
    path("listing/<int:id>/close/", views.close_listing, name="close_listing"),
    path("listing/<int:id>/comment", views.add_comment, name="comment"),
    path("listing/<str:username>/watchlist/", views.watch_listing, name="watch_listing"),
    path("listing/<int:id>/watchlist/add", views.add_watch_list, name="add_watch_list"),
]
