import urllib2
import json

def authenticate(username, apikey):

    request = urllib2.Request("https://identity.api.rackspacecloud.com/v2.0/tokens")

    request.add_header('Content-type', 'application/json')

    data = json.dumps({ "auth": { "RAX-KSKEY:apiKeyCredentials": { "username": username, "apiKey": apikey } } })

    response = urllib2.urlopen(request, data=data)

    jsn = json.loads(response.read())
    return jsn['access']['token']['id']
