from django.forms import ModelForm


from .models import Category, AuctionListing

CATEGORIES = Category.objects.all()


""" class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    description = forms.CharField(label="Description")
    start_bid = forms.FloatField()
    category= forms.CharField(label='Category', widget=forms.Select(choices=CATEGORIES))
    image = forms.URLField() """
    
class NewListingForm(ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'start_bid', 'category', 'image']