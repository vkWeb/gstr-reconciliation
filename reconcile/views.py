import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from reconcile import utils


def index(request):
    return HttpResponse("API Server Running.")


@csrf_exempt
def process(request):
    if request.method == "POST":
        gstr2b = request.FILES["gstr2b-json"]
        csvfile = request.FILES["purchase-register-csv"]
        # read() not for big files but we are only dealing with text files so it is fine
        utils.save_file(f"{gstr2b.name}", gstr2b.read())
        utils.save_file(f"{csvfile.name}", csvfile.read())
    return HttpResponse()


def json_and_csv(request, jtitle, ctitle):
    j = open(f"gst/{jtitle}")
    load_j = json.load(j)
    json_dict = {}
    for x in load_j["data"]["docdata"]["b2b"]:
        json_dict[str(x["ctin"]) + "".join([str(i["inum"]) for i in x["inv"]])] = {}
        print()
    """ for x in y["data"]["docdata"]["b2b"]:
            print(f"value = {str(x['ctin'])+''.join([str(i['inum']) for i in x['inv']])}") """
    """ fields = []
    rows = []
    c = open(f'gst/{ctitle}')
    load_c = csv.reader(c)
    csvdict = {} """
