from django.shortcuts import HttpResponse, HttpResponseRedirect,render
from . import util
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request,"app/index.html")

@csrf_exempt
def process(request):
    if request.method == 'POST':
        gstr2b = request.FILES["gstr2b-json"]
        csvfile = request.FILES["purchase-register-csv"]
        #read() not for big files but we are only dealing with text files so it is fine
        util.save_file(f"{gstr2b.name}",gstr2b.read()) 
        util.save_file(f"{csvfile.name}",csvfile.read()) 
    return render(request,"app/index.html")
