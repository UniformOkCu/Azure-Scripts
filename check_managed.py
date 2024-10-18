import argparse
import requests
import xml.etree.ElementTree as ET
import json

def check_managed(domain):
    res = requests.get(f"https://login.microsoftonline.com/getuserrealm.srf?login={domain}&xml=1")
    xml = res.content

    xml_str = xml.decode("utf-8")
    root = ET.fromstring(xml_str)

    namespace_type = root.find('NameSpaceType')

    if namespace_type.text == "Managed":
        return True
    else:
        return False
    
    return None

def get_tenant_id(domain):
    res = requests.get(f"https://login.microsoftonline.com/{domain}/.well-known/openid-configuration")
    data = res.content

    json_str = data.decode('utf-8')

    json_data = json.loads(json_str)

    token_endpoint = json_data['token_endpoint']

    tenant_id = str(token_endpoint).split(".com/")[1].split("/")[0]

    return tenant_id
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help="Domain to check", required=True)

    args = parser.parse_args()
    domain = args.domain

    if (check_managed(domain)):
        print(get_tenant_id(domain))
    else:
        print(f"{domain} not managed")