import json
import urllib2
from auth import authenticate
from os import path

class Servers(object):
    def __init__(self, username, apikey, tenant):
        self.tenant = tenant
        self.endpoint = "https://iad.servers.api.rackspacecloud.com/v2/%s" % tenant
        self.username = username
        self.apikey = apikey
        self.token = authenticate(username, apikey)
    
    def get_servers(self):
        url = path.join(self.endpoint, 'servers')
        request = urllib2.Request(url)

        request.add_header('X-Auth-Token', self.token)

        response = urllib2.urlopen(request)
        jsn = json.loads(response.read())
        for server in jsn['servers']:
            yield("""
Server Name: %(name)s
UUID: %(id)s
Links: %(links)s
""" % server )

    def __str__(self):
        printer = []
        for server in self.get_servers():
            printer.append(server)

        return "\n".join(printer)

    def get_server_id(self, name):
        url = path.join(self.endpoint, 'servers?name=%s' % name)
        request = urllib2.Request(url)
        request.add_header('X-Auth-Token', self.token)

        response = urllib2.urlopen(request)

        jsn = json.loads(response.read())
        return jsn['servers'][0]['id']
    
    def get_private_ip(self, name):
        url = path.join(self.endpoint, 'servers/%s/ips' % self.get_server_id(name))
        request = urllib2.Request(url)
        request.add_header('X-Auth-Token', self.token)

        response = urllib2.urlopen(request)

        jsn = json.loads(response.read())
        return jsn['addresses']['private'][0]['addr']

    def get_metadata(self, name):
        url = path.join(self.endpoint, 'servers/%s' % self.get_server_id(name))
        request = urllib2.Request(url)
        request.add_header('X-Auth-Token', self.token)

        response = urllib2.urlopen(request)

        jsn = json.loads(response.read())
        return jsn['server']['metadata']
