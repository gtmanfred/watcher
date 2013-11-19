import json
from auth import authenticate
import urllib2
from os import path
from servers import Servers
from queuemessages import QueueMessages
import chef

class Knife(Servers):
    def __init__(self, username, apikey, tenant):
        super(self.__class__, self).__init__(username, apikey, tenant)
        self.queue = QueueMessages(username, 'daniel-scalinggroup', token=self.token)

    def watch(self):
        api = chef.autoconfigure()
        for server in self.queue.get_messages():
            instance = self.get_metadata(server)
            node = chef.Node(server)
            node.run_list.append('role[%s]' % instance)
            node.save()
