import json

from asgiref.sync import async_to_sync
from channels.auth import AuthMiddlewareStack
from channels.generic.websocket import WebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path


class MessageConsumer(WebsocketConsumer):

    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # Can access logged in user details by using self.scope.user,
            # Can only be used if AuthMiddlewareStack is used in the routing.py
            # print(self.scope["user"])
            # Setting the group name as the pk of the user primary key as it is unique to each user.
            #  The group name is used to communicate with the user.
            self.group_name = str(self.scope["user"].pk)
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()

    def disconnect(self, close_code):
        pass

    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    def notify(self, data):
        self.send(text_data=json.dumps({
            'message': data['text'],
            'notification_id': data['notification_id'],
        }))


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            [re_path(r'ws/notifs/$', MessageConsumer)]
        )
    ),
})
