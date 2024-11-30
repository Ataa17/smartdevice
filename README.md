Real-Time Sensor Data Monitoring System
This project provides a system to monitor real-time data from an Arduino-based sensor device using WebSockets and Django. It captures data sent by the Arduino, processes it on the Django server, and displays it in real-time on a web interface.

System Architecture
Components
Arduino (Sensor Device)

Collects data from sensors (e.g., temperature, distance, RGB light states).
Sends data to the server via WebSocket communication.
Django Server

Hosts the backend application, processes incoming data, and stores it in a database.
Implements WebSocket endpoints to receive data and broadcast updates to the web interface.
Web Interface

Displays real-time sensor data dynamically on the dashboard using WebSockets.
Data Flow
Sensor Data Collection

Arduino gathers data from connected sensors.
Sends the data in JSON format through a WebSocket connection to the Django server.
Django Backend

Processes the incoming WebSocket messages using Django Channels.
Updates the database with the latest sensor data.
Broadcasts the updated data to all connected clients (the web dashboard).
Web Dashboard

A real-time web interface subscribes to WebSocket updates.
Dynamically updates the displayed sensor values without refreshing the page.
Data Format
The Arduino should send sensor data as a JSON object in the following format:

{
    "temp": 25.5,         // Temperature in °C
    "distance": 150.2,    // Distance in cm
    "red": true,          // RGB Red Light ON/OFF
    "green": false,       // RGB Green Light ON/OFF
    "blue": true          // RGB Blue Light ON/OFF
}
Arduino Communication Requirements
1. WebSocket Communication
The Arduino should use a library like ArduinoWebsockets for WebSocket communication.

2. Connection Setup
The Arduino needs to connect to the Django WebSocket server at:

ws://<SERVER_IP>:8000/ws/sensor/
Example Code Snippet:

#include <WiFi.h>
#include <ArduinoWebsockets.h>

using namespace websockets;

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* websocketServer = "192.168.1.100"; // Replace with your server's IP
const int port = 8000;

WebsocketsClient client;

void setup() {
    Serial.begin(115200);
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // Connect to WebSocket server
    client.onMessage([](WebsocketsMessage message) {
        Serial.println("Message from server: " + message.data());
    });

    client.connect(websocketServer, port, "/ws/sensor/");
    Serial.println("Connected to WebSocket server");
}

void loop() {
    // Example sensor data
    float temperature = 26.5;
    float distance = 120.4;
    bool redLight = true;
    bool greenLight = false;
    bool blueLight = true;

    // Format data as JSON
    String jsonData = "{";
    jsonData += "\"temp\":" + String(temperature) + ",";
    jsonData += "\"distance\":" + String(distance) + ",";
    jsonData += "\"red\":" + String(redLight ? "true" : "false") + ",";
    jsonData += "\"green\":" + String(greenLight ? "true" : "false") + ",";
    jsonData += "\"blue\":" + String(blueLight ? "true" : "false");
    jsonData += "}";

    // Send data to server
    client.send(jsonData);

    // Keep connection alive
    client.poll();

    delay(1000); // Adjust this to control data sending frequency
}
Backend Setup
Run the Django Server

Start the server using Daphne:
daphne -b 0.0.0.0 -p 8000 smartdevice.asgi:application
API Endpoint

The Arduino connects to the WebSocket endpoint:
ws://<SERVER_IP>:8000/ws/sensor/
Database

Sensor data is stored in the Summary model in the database.
Web Interface

Access the real-time dashboard at:
http://<SERVER_IP>:8000/
Important Notes for Arduino Developer
Data Transmission Rate

Avoid sending data too frequently (e.g., every millisecond) to reduce server load. Sending data every 1-5 seconds is recommended.
Error Handling

Handle potential WebSocket disconnections and attempt reconnections in your Arduino code.
Network Configuration

Ensure the Arduino is on the same local network as the Django server or configure the server to accept connections from external networks.
Troubleshooting
If the dashboard does not update:

Check that the Arduino is successfully connected to the WebSocket server.
Verify that the Django server is running and accessible.
Check the browser console for WebSocket errors.
Use logs on both the Arduino and Django server to debug issues.

