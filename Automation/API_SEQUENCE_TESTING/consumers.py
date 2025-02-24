from channels.generic.websocket import AsyncWebsocketConsumer
import json
import logging
logger = logging.getLogger(__name__)


class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.group_name = 'transaction_group'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            logger.error(f"Error during connect: {e}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            # Handle data...
        except Exception as e:
            logger.error(f"Error during receive: {e}")