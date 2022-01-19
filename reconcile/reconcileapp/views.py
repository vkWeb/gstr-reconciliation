from django.shortcuts import HttpResponse, HttpResponseRedirect,render
from django.core.files.storage import default_storage

def index(request):
    return render(request,"app/debug.html")

def process(request):
    return render(request,"app/index.html")
