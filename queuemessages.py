import json
from auth import authenticate
from os import path
import urllib2
import socket

class QueueMessages(object):
    def __init__(self, username, queue, apikey=None, token=None):
        self.endpoint = "https://iad.queues.api.rackspacecloud.com/"
        self.queue = queue
        self.username = username
        self.apikey = apikey
        if token : 
            self.token = token
        else:
            self.token = authenticate(username, apikey)

    def get_messages(self):
        url = path.join(self.endpoint, "v1/queues/%s/messages?echo=true" % self.queue)
        request = urllib2.Request(url)

        request.add_header('Content-type', 'application/json')
        request.add_header('X-Auth-Token', self.token)
        request.add_header('Client-ID', 'e58668fc-26eb-11e3-8270-5b3128d43830')
        request.add_header('Accept', 'application/json')

        response = urllib2.urlopen(request)

        jsn = json.loads(response.read())

        for server in jsn['messages']:
            try:
                yield server['body']['hostname']
            except:
                pass
            finally:
                self.delete_message(server['href'][1:])

    def delete_message(self, messageid):
        url = path.join(self.endpoint, messageid)
        request = urllib2.Request(url)

        request.add_header('Content-type', 'application/json')
        request.add_header('X-Auth-Token', self.token)
        request.add_header('Client-ID', 'e58668fc-26eb-11e3-8270-5b3128d43830')
        request.add_header('Accept', 'application/json')

        request.get_method = lambda: 'DELETE'

        response = urllib2.urlopen(request)

    def post_message(self, hostname):
        url = path.join(self.endpoint, "v1/queues/%s/messages" % self.queue)
        request = urllib2.Request(url)

        request.add_header('Content-type', 'application/json')
        request.add_header('X-Auth-Token', self.token)
        request.add_header('Client-ID', 'e58668fc-26eb-11e3-8270-5b3128d43830')
        request.add_header('Accept', 'application/json')

        data = json.dumps([{ "ttl": 300, "body": { "hostname": hostname} }])
        data = data.encode('utf-8')
        request.add_data(data)

        response = urllib2.urlopen(request)
