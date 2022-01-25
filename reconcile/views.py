import json, csv

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from reconcile import utils


def index(request):
    return HttpResponse("API Server Running.")


@csrf_exempt
def reconcile(request):
    if request.method == "POST":
        gstr2b = request.FILES["gstr2b-json"]
        csvfile = request.FILES["purchase-register-csv"]
        # read() not for big files but we are only dealing with text files so it is fine
        utils.save_file(f"{gstr2b.name}", gstr2b.read())
        utils.save_file(f"{csvfile.name}", csvfile.read())
        resultant = build_dict(gstr2b.name,csvfile.name)
        JsonResponse(resultant)
    return HttpResponse()


def build_dict(jtitle, ctitle):
    f = open(f"gst/{jtitle}")
    load_f = json.load(f)
    json_dict = {}
    for x in load_f["data"]["docdata"]["b2b"]:
        for i in x["inv"]:
            for j in i["items"]:
                if(j["rt"] != 0):
                    if(j.get("igst") is not None and j["igst"] != 0):
                        json_dict[str(x["ctin"]) + "".join([str(i["inum"])])] = {
                            "date": str(i["dt"]), 
                            "tax_val": str(j["txval"]), 
                            "rate": str(j["rt"]),
                            "supply_type": "INTER"}
                    else:
                        json_dict[str(x["ctin"]) + "".join([str(i["inum"])])] = {
                            "date": str(i["dt"]), 
                            "tax_val": str(j["txval"]), 
                            "rate": str(j["rt"]),
                            "supply_type": "INTRA"}
    f.close()
    #utils.save_file(f"new.json",json.dumps(json_dict))


    c = open(f'gst/{ctitle}')
    load_c = csv.DictReader(c)
    csv_dict = {}
    for row in load_c:
        if (row["Rate (%)"] != 0):
            if(row["Central Tax"] != 0 and row["State/UT tax"] != 0):
                csv_dict[str(row["GSTIN of supplier"]+row["Invoice number"])] = {
                    "date": str(row["Invoice Date"]).strip(), 
                    "tax_val": str(row["Taxable Value"]).strip(), 
                    "rate": str(row["Rate (%)"]).strip(),
                    "supply_type": "INTRA"}
            else:
                csv_dict[str(row["GSTIN of supplier"]+row["Invoice number"])] = {
                    "date": str(row["Invoice Date"]).strip(), 
                    "tax_val": str(row["Taxable Value"]).strip(), 
                    "rate": str(row["Rate (%)"]).strip(),
                    "supply_type": "INTER"}
    #utils.save_file(f"newcsvc.json",json.dumps(csv_dict))
    c.close()
    return match(json_dict,csv_dict)        


def match(json_dict,csv_dict):
    not_in_csv = {}
    not_in_json = {} 
    matched = {}
    mismatch = {}
    for key in csv_dict:
        if (json_dict.get(key) is not None) and (csv_dict[key] == json_dict[key]):
            matched[key] = csv_dict[key]
            #del csv_dict[key]
            del json_dict[key]
        elif(json_dict.get(key) is not None) and (csv_dict.get(key) is not None) and (csv_dict[key] != json_dict[key]):
            mismatch[key] = csv_dict[key]
        else:
            not_in_json[key] = csv_dict[key]
    del csv_dict
    not_in_csv = json_dict
    del json_dict
    the_ultimate_dict = {}
    the_ultimate_dict["MATCHED"] = matched
    the_ultimate_dict["MISMATCHED"] = mismatch
    the_ultimate_dict["MISSING_IN_CSV"] = not_in_csv
    the_ultimate_dict["MISSING_IN_JSON"] = not_in_json

    #utils.save_file(f"ultimate.json",json.dumps(the_ultimate_dict))

    return the_ultimate_dict

build_dict('2b.json','purchase.csv')