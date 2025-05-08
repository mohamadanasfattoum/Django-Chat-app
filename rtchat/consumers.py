from channels.generic.websocket import WebsocketConsumer


class ChatroomConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()  # Accept the WebSocket connection


# Diese Klasse ist der Einstiegspunkt für die Verwaltung von WebSocket-Verbindungen.
#  Sie kann erweitert werden, um Nachrichten zu senden, zu empfangen und Benutzer zu Gruppen hinzuzufügen.
