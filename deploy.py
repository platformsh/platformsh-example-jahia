import json
import base64
import os
import requests
from requests.auth import HTTPBasicAuth

# Edit these as needed.
DX_USERNAME = 'root'
DX_PASSWORD = 'root'
DX_RELATIONSHIP = 'jahia'

def send_install_request(filename):
    with open(filename, 'rb') as jar_handle:
        files = {"bundle": jar_handle}
        data = {'start': 'true'}
        url = dx_rest_url()
        response = requests.post(url, files=files, data=data, auth=HTTPBasicAuth(DX_USERNAME, DX_PASSWORD))
        response.raise_for_status()
        print "Plugin {} installed and started successfully.".format(filename)

def install_plugins(commands):
    if 'install' in commands.keys():
        for filename in commands['install']:
            send_install_request(filename)

def uninstall_plugins(commands):
    pass
#    if 'install' in commands.keys():
#        for filename in commands['uninstall']:
#            send_install_request(filename)

def dx_rest_url():
    platform_relationships = os.getenv('PLATFORM_RELATIONSHIPS')
    if platform_relationships:
        relationships = json.loads(base64.b64decode(platform_relationships).decode('utf-8'))

        # Extract the relationships that we want to expose to the application.
        jahia = relationships[DX_RELATIONSHIP][0]

        url = "http://{}:{}/modules/api/bundles/".format(
            jahia['host'],
            jahia['port'],
        )
        return url

def run():
    with open('deploy.json', 'r') as json_file:
        commands = json.load(json_file)

    install_plugins(commands)
    uninstall_plugins(commands)

run()
