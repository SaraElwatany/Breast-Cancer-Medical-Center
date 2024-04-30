# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer


class DoctorWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.send(
            text_data=json.dumps({
                'type': 'Connection_established',
                'message': 'You Are Now Connected !!'
            })
        )

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Process incoming HL7 message from the patient
        # Here you can parse the HL7 message, extract appointment details,
        # and save them to the database or perform any necessary actions
        print(text_data)
        pass

