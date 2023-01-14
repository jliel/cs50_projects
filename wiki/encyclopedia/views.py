from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect

import random
import markdown2

from . import util
from .forms import SearchForm, NewPageForm, EditPageForm

searchForm = SearchForm()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": searchForm
    })
    
def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry_page', args=[title]))
    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {"newForm": form, "form": searchForm})

def edit_entry(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        editForm = EditPageForm(request.POST)
        if editForm.is_valid():
            title = title.capitalize()
            content = editForm.cleaned_data["content"].strip()
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('entry_page', args=[title]))
    else:
        editForm = EditPageForm(initial={"content": entry})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "editForm": editForm,
        "form": searchForm
    })

def entry_page(request, title):
    entry = util.get_entry(title)
    content = ""
    if entry:
        title = entry.split()[1]
        content = markdown2.markdown(entry)
    else:
        title = "PageNotFound"
    return render(request, "encyclopedia/entry_page.html", {
        "entry": content,
        "title": title,
        "form": searchForm
    })

def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return HttpResponseRedirect(reverse('entry_page', args=[entry]))
    
def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["q"]
            entries = [entry.lower() for entry in util.list_entries()]
            if query.lower() in entries:
                return HttpResponseRedirect(reverse('entry_page', args=[query]))
            else:
                recommended = []
                for entry in entries:
                    if query in entry:
                        recommended.append(entry)
                return render(request, "encyclopedia/search.html", 
                              {"form": form, "query": query, "recommended": recommended})
    else:
        form = SearchForm()
    return render(request, "encyclopedia/layout.html", {"form": searchForm})