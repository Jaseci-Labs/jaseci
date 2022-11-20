import json
import sys

module = sys.argv[1]
with open("temp.json", "r") as fin:
    yaml = json.load(fin)
dic = {}
for v in yaml["items"]:
    dic[v["kind"]] = v
dic = {"module": f"jaseci_ai_kit.{module}", "remote": dic}
dic_str = json.dumps(dic)
dic_str = dic_str.replace("null", "None")
dic_str = dic_str.replace("js-", "jaseci-")
print(f"{module.upper()}_ACTION_CONFIG = " + dic_str)
