from django.shortcuts import HttpResponse, HttpResponseRedirect,render
from . import util
from django.views.decorators.csrf import csrf_exempt
import json ,csv

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

def json_and_csv(request,jtitle,ctitle):
    j = open(f'gst/{jtitle}')
    load_j = json.load(j)
    json_dict = {}
    for x in load_j["data"]["docdata"]["b2b"]:
        json_dict[str(x['ctin'])+''.join([str(i['inum']) for i in x['inv']])] = {}
        print()
    """ for x in y["data"]["docdata"]["b2b"]:
            print(f"value = {str(x['ctin'])+''.join([str(i['inum']) for i in x['inv']])}") """
    """ fields = []
    rows = []
    c = open(f'gst/{ctitle}')
    load_c = csv.reader(c)
    csvdict = {} """