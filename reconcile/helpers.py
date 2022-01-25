import json
import csv


def build_dict(gstr2b_file_handler, csv_file_handler):
    load_f = json.load(gstr2b_file_handler)
    json_dict = {}
    for x in load_f["data"]["docdata"]["b2b"]:
        for i in x["inv"]:
            for j in i["items"]:
                if j["rt"] != 0:
                    if j.get("igst") is not None and j["igst"] != 0:
                        json_dict[str(x["ctin"]) + "".join([str(i["inum"])])] = {
                            "gstin": str(x["ctin"]),
                            "inv_num": str(i["inum"]),
                            "date": str(i["dt"]),
                            "tax_val": float(j["txval"]),
                            "rate": int(j["rt"]),
                            "supply_type": "INTER",
                        }
                    else:
                        json_dict[str(x["ctin"]) + "".join([str(i["inum"])])] = {
                            "gstin": str(x["ctin"]),
                            "inv_num": str(i["inum"]),
                            "date": str(i["dt"]),
                            "tax_val": float(j["txval"]),
                            "rate": int(j["rt"]),
                            "supply_type": "INTRA",
                        }

    decoded_file = csv_file_handler.read().decode("utf-8").splitlines()
    load_c = csv.DictReader(decoded_file)
    csv_dict = {}
    for row in load_c:
        if row["Rate (%)"] != 0:
            if row["Central Tax"] != 0 and row["State/UT tax"] != 0:
                csv_dict[str(row["GSTIN of supplier"] + row["Invoice number"])] = {
                    "gstin": str(row["GSTIN of supplier"]).strip(),
                    "inv_num": str(row["Invoice number"]).strip(),
                    "date": str(row["Invoice Date"]).strip(),
                    "tax_val": float(row["Taxable Value"].strip()),
                    "rate": int(row["Rate (%)"].strip()),
                    "supply_type": "INTRA",
                }
            else:
                csv_dict[str(row["GSTIN of supplier"] + row["Invoice number"])] = {
                    "gstin": str(row["GSTIN of supplier"]).strip(),
                    "inv_num": str(row["Invoice number"]).strip(),
                    "date": str(row["Invoice Date"]).strip(),
                    "tax_val": float(row["Taxable Value"].strip()),
                    "rate": int(row["Rate (%)"].strip()),
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
        elif json_dict.get(key) == csv_dict[key]:
            matched.append(csv_dict[key])
            del json_dict[key]
        else:
            mismatch.append(csv_dict[key])

    for key in json_dict:
        not_in_csv.append(json_dict[key])

    return {
        "matched": matched,
        "mismatched": mismatch,
        "missing_in_csv": not_in_csv,
        "missing_in_json": not_in_json,
    }
