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
    """
    API Endpoint: /api/reconcile/

    Reconciles the entries of GSTR-2B JSON data and purchase register's CSV.
    """
    if request.method == "POST":
        gstr2b = request.FILES["gstr2b-json"]
        csvfile = request.FILES["purchase-register-csv"]
        json_dict, csv_dict = build_dict(gstr2b, csvfile)
        result = match(json_dict, csv_dict)
        return JsonResponse(result)
    else:
        return HttpResponseNotAllowed(["POST"])
