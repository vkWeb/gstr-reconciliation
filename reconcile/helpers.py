import json
import csv

from decimal import Decimal
from datetime import datetime


def build_dict(gstr2b_file_handler, csv_file_handler):
    load_f = json.load(gstr2b_file_handler)
    json_dict = {}

    for supplier in load_f["data"]["docdata"]["b2b"]:
        for inv in supplier["inv"]:
            for inv_item in inv["items"]:
                if inv_item["rt"] > 0:
                    if inv_item.get("igst") is not None and Decimal(inv_item["igst"]) > 0.00:
                        json_dict[str(supplier["ctin"] + inv["inum"])] = {
                            "gstin": supplier["ctin"],
                            "inv_num": inv["inum"],
                            "date": inv["dt"],
                            "taxable_value": str(inv_item["txval"]),
                            "rate": inv_item["rt"],
                            "supply_type": "INTER",
                        }
                    else:
                        json_dict[str(supplier["ctin"] + inv["inum"])] = {
                            "gstin": supplier["ctin"],
                            "inv_num": inv["inum"],
                            "date": inv["dt"],
                            "taxable_value": str(inv_item["txval"]),
                            "rate": inv_item["rt"],
                            "supply_type": "INTRA",
                        }

    decoded_file = csv_file_handler.read().decode("utf-8").splitlines()
    load_c = csv.DictReader(decoded_file)
    csv_dict = {}
    
    for row in load_c:
        if int(row["Rate"]) > 0:
            inv_date_obj = datetime.strptime(row["Invoice date"], "%d-%b-%Y").date()
            inv_date_fstr = inv_date_obj.strftime("%d-%m-%Y")
            
            if Decimal(row["State/UT Tax Paid"]) > 0.00:
                csv_dict[str(row["GSTIN of Supplier"] + row["Invoice Number"])] = {
                    "gstin": row["GSTIN of Supplier"],
                    "inv_num": row["Invoice Number"],
                    "date": inv_date_fstr,
                    "taxable_value": str(row["Taxable Value"]),
                    "rate": int(row["Rate"]),
                    "supply_type": "INTRA",
                }
            else:
                csv_dict[str(row["GSTIN of Supplier"] + row["Invoice Number"])] = {
                    "gstin": row["GSTIN of Supplier"],
                    "inv_num": row["Invoice Number"],
                    "date": inv_date_fstr,
                    "taxable_value": str(row["Taxable Value"]),
                    "rate": int(row["Rate"]),
                    "supply_type": "INTER",
                }

    return json_dict, csv_dict


def match(json_dict, csv_dict):
    not_in_csv = []
    not_in_json = []
    matched = []
    mismatch = []

    for key in csv_dict:
        if json_dict.get(key) is None:
            not_in_json.append(csv_dict[key])
            continue
        elif json_dict.get(key) == csv_dict[key]:
            matched.append(csv_dict[key])
        else:
            mismatch.append(csv_dict[key])
        del json_dict[key]

    for key in json_dict:
        not_in_csv.append(json_dict[key])

    return {
        "matched": matched,
        "mismatched": mismatch,
        "missing_in_csv": not_in_csv,
        "missing_in_json": not_in_json,
        "total_invoices": len(not_in_csv) + len(not_in_json) + len(matched) + len(mismatch),
    }
