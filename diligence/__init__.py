import requests
import argparse
import json


KNOWN_LICENSES = {
    'BSD': 'http://opensource.org/licenses/BSD-2-Clause',
    'MIT': 'http://opensource.org/licenses/MIT',
    'ZPL': 'http://opensource.org/licenses/ZPL-2.0',
    'PSF': 'http://opensource.org/licenses/Python-2.0',
    'LGPL': 'http://opensource.org/licenses/LGPL-3.0',
    'Apache': 'http://opensource.org/licenses/Apache-2.0',
    'UNKNOWN': '-',
}

def link_to(license):
    if license in KNOWN_LICENSES:
        return KNOWN_LICENSES[license], 1.0


    # try to find a license in the license string somewhere..
    for k,v in KNOWN_LICENSES.items():
        if license.find(k) != -1:
            return v, 0.8

    return "", 0.0

def get_license(package):
    url = "http://pypi.python.org/pypi/{}/json".format(package)

    resp = requests.get(url)

    if resp.status_code != 200:
        return None

    data = json.loads(resp.content)
    license = data['info']['license']
    return license.replace("\n","").replace('"', '\\"')


def process_file(filename):
    f = open(filename, 'r')
    found = []
    not_found = []

    for line in f:
        package = line.split("==")[0]
        license = get_license(package)
        if license:
            found.append({'package': package, 'license': license})
        else:
            not_found.append(package)

    print "Package,License,Url,Score"
    for item in found:
        url, score = link_to(item['license'])
        print "{},\"{}\",{},{}".format(item['package'], item['license'], url, score)


    if len(not_found) > 0:
        print ""
        print "Packages Not Found"
        print "------------------"
        for item in not_found:
            print item

def main():
    parser = argparse.ArgumentParser(description='Scan requirement files for license information')
    parser.add_argument('-r', dest='requirements', required=True,
                        help='a requirements file to read for license information')

    args = parser.parse_args()
    process_file(args.requirements)
