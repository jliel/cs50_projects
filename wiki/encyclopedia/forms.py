from django import forms

from .util import list_entries


class SearchForm(forms.Form):
    q = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))


class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", max_length=20)
    content = forms.CharField(label="Content", 
                              widget=forms.Textarea(attrs={'rows':3, 'class': 'content_label'}))
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        entries = list_entries()
        entries = [entry.lower() for entry in entries]
        
        if title.lower() in entries:
            msg = f"A page with the title '{title}' already exists, try another one."
            self.add_error('title', msg)


class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", 
                              widget=forms.Textarea(attrs={'class': 'content_label'}))
    
