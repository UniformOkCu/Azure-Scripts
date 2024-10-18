import argparse
import requests
import xml.etree.ElementTree as ET

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help="Domain to check", required=True)

    args = parser.parse_args()
    domain = args.domain

    if (check_managed(domain)):
        print(f"{domain} is managed.")
    else:
        print(f"{domain} is NOT managed.")