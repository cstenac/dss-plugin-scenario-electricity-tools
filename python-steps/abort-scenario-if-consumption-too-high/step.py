import os, json, requests, json
from dataiku.customstep import *

plugin_config = json.loads(os.environ["DKU_PLUGIN_CONFIG"])
step_config = get_step_config()

#print(step_config)
login =plugin_config["config"]["rte_credentials"]["rte_credentials"]['user']
password =plugin_config["config"]["rte_credentials"]["rte_credentials"]['password']

token_url = "https://digital.iservices.rte-france.com/token/oauth"

access_token = requests.post(token_url, auth=(login,password)).json()["access_token"]

print("AT=%s" % access_token)
url = "https://digital.iservices.rte-france.com/open_api/consumption/v1/short_term?type=REALISED"

resp = requests.get(url, headers= {'Authorization': 'Bearer ' + access_token})

#print(resp)
data = resp.json()

print("\n\n" + json.dumps(data))
points = data["short_term"][0]["values"]

point = points[len(points)-1]

print("POINT: %s" % point)

if point["value"] > step_config.get("threshold"):
    raise Exception("Electricity consumption is too high (%s MW), aborting run" % point["value"])