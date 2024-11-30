import serial
import asyncio
import websockets
import json

arduino_port = 'COM3'
baud_rate = 9600
websocket_url = 'ws://localhost:8000/ws/sensor/'

async def send_data():
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    async with websockets.connect(websocket_url) as websocket:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"Sensor Data: {line}")
                if "Temp" in line:
                    # Parse data
                    parts = line.split(',')
                    temperature = float(parts[0].split(': ')[1].replace('°C', ''))
                    humidity = float(parts[1].split(': ')[1].replace('%', ''))
                    data = {"temperature": temperature, "humidity": humidity}
                    await websocket.send(json.dumps(data))
                    print("Data sent to WebSocket")

asyncio.run(send_data())
