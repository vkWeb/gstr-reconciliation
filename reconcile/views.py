from django.http import HttpResponse 
from django.http import JsonResponse
from django.http import HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from reconcile.helpers import build_dict
from reconcile.helpers import match

def index(request):
    return HttpResponse("API Server Running.")


@csrf_exempt
def reconcile(request):
    if request.method == "POST":
        gstr2bfile = request.FILES["gstr2b-json"]
        csvfile = request.FILES["purchase-register-csv"]
        
        json_dict, csv_dict = build_dict(gstr2bfile, csvfile)
        result = match(json_dict, csv_dict)
        return JsonResponse(result)
    else:
        return HttpResponseNotAllowed()
