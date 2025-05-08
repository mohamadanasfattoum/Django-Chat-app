from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
import json  # Import JSON for parsing incoming messages
from django.template.loader import render_to_string  # Import for rendering templates
from asgiref.sync import async_to_sync  # Import for synchronous channel layer operations
from .models import ChatGroup, GroupMessages  # Import your models




class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]  # Get the user from the scope
        self.chatroom_name = self.scope["url_route"]["kwargs"]["chatroom_name"] # Get the chatroom name from the URL
        self.chatroom = get_object_or_404(ChatGroup, group_name=self.chatroom_name)  # Get the chatroom object from the database

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,  # The name of the chatroom group
            self.channel_name  # The channel name for this WebSocket connection
        )

        self.accept()  # Accept the WebSocket connection

    def disconnect(self, close_code):
        # Handle disconnection from the WebSocket
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,  # The name of the chatroom group
            self.channel_name  # The channel name for this WebSocket connection
        )


    def receive(self, text_data):
        # Handle incoming messages from the WebSocket
        text_data_json = json.loads(text_data)  # Parse the incoming JSON data
        body = text_data_json['body']  # Extract the message body from the JSON data
        # Here you would typically save the message to the database

        message = GroupMessages.objects.create(
            body=body,
            author=self.user,  # Associate the message with the user
            group=self.chatroom  # Associate the message with the chatroom
        )

        event = {
            'type': 'message_handler',  # The type of event to handle
            'message_id': message.id,  # The ID of the message
        }

        # Send the message to the chatroom group
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name, event # The name of the chatroom group

        )

    def message_handler(self, event):
        message_id = event['message_id']
        message = GroupMessages.objects.get(id=message_id)  # Get the message object from the database
        context = {
            'message': message,  # Pass the message object to the template
            'user': self.user,  # Pass the user object to the template
        }

        html = render_to_string("rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)


# Diese Klasse ist der Einstiegspunkt für die Verwaltung von WebSocket-Verbindungen.
#  Sie kann erweitert werden, um Nachrichten zu senden, zu empfangen und Benutzer zu Gruppen hinzuzufügen.
