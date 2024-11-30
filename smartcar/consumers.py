import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Summary
from datetime import datetime


class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.is_reading = True
        # Start a background task to read sensor data
        asyncio.create_task(self.read_sensor_data())

    async def disconnect(self, close_code):
        self.is_reading = False

    async def read_sensor_data(self):
        while self.is_reading:
            # Simulate receiving data (replace this with actual sensor readings)
            fake_data = {
                "temperature": 25.5,  # Example temperature
                "red": True,  # Example RGB value for red (True/False)
                "green": False,  # Example RGB value for green
                "blue": True,  # Example RGB value for blue
                "distance": 120.0  # Example distance in cm
            }

            # Save data to database
            summary = Summary.objects.create(
                temp=fake_data["temperature"],
                Red=fake_data["red"],
                Green=fake_data["green"],
                Blue=fake_data["blue"],
                distance=fake_data["distance"]
            )

            # Send data to WebSocket
            await self.send(text_data=json.dumps({
                "temperature": fake_data["temperature"],
                "red": fake_data["red"],
                "green": fake_data["green"],
                "blue": fake_data["blue"],
                "distance": fake_data["distance"],
                "timestamp": datetime.now().isoformat()  # Send timestamp in ISO format
            }))
            await asyncio.sleep(0.1)  # Send data every second
