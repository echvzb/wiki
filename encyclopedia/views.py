from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "page_active":"home"
    })


def title(request, title):
    entry = util.get_entry(title)

    if entry is not None:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(entry),
            "title": title,
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found."
        })


def search(request):
    q = request.GET['q'].lower()
    entries = util.list_entries()
    results = []
    for entry in entries:
        temp = entry
        temp = temp.lower()
        if temp.find(q) != -1:
            results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "entries": results,
        'title': 'Search',
    })


def new(request):
    if request.method == 'POST':
        title = request.POST['title']

        if util.get_entry(title) is None:
            content = request.POST['content']
            util.save_entry(title, content)
            return render(request, 'encyclopedia/editPage.html', {
                'title': 'New',
                'action': 'Add new page',
                'alert': 'Successfully added new page.',
                "page_active":"new"
            })
        return render(request, 'encyclopedia/error.html',{
            'error': 'Page: ' + title + " alredy exists."
        })

    return render(request, 'encyclopedia/editPage.html', {
        'title': 'New',
        'action': 'Add new page',
        "page_active":"new"

    })

def randomPage(request):
    entries = util.list_entries()
    i = random.randint(0,len(entries)-1)
    return HttpResponseRedirect(reverse('title', args=(entries[i],)))

def edit(request, title):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title,content)

        return HttpResponseRedirect(reverse('title', args=(title,)))

    return render(request, 'encyclopedia/editPage.html',{
        'title':'Edit',
        'action':'Edit page',
        'title_entry': title,
        'content_entry': util.get_entry(title),
        'page_active':'edit'

    })

        
