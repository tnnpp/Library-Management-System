from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


def home(request):
    return render(request, 'library/home.html')

def search(request):
    if request.method == 'POST':
        query = request.POST['query']
        results = Books.objects.filter(title__contains=query)
        return render(request, 'library/search.html', {'results': results})
