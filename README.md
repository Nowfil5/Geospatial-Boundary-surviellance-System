# Geospatial Boundary Surveillance for Coastal Fishermen

This project is a maritime boundary monitoring system that combines an Arduino-based GPS/LoRa transmitter, a LoRa receiver, and a Python dashboard to visualize boat position on a map and flag boundary violations.

## Project Structure

- `DashBoard/dynamicdashboard.py` - Interactive dashboard where boundary points can be added and confirmed in the UI.
- `DashBoard/final_dashborad.py` - Dashboard with a predefined maritime boundary polygon.
- `IoT Files/Transmitter/Transmitter.ino` - Reads GPS data and sends latitude/longitude over LoRa.
- `IoT Files/Receiver/Receiver.ino` - Receives LoRa packets and prints GPS coordinates to the serial port.

## How It Works

1. The transmitter reads location data from a GPS module using `TinyGPS++`.
2. The transmitter sends latitude and longitude over a LoRa radio link.
3. The receiver reads the LoRa packets and forwards the coordinates to the computer through Serial.
4. The Python dashboard reads the serial data, plots the boat position on a map, and marks it as safe or alert based on the configured maritime boundary.

## Requirements

### Python dashboard

- Python 3.9 or newer
- `pyserial`
- `tkintermapview`
- `shapely`
- `Pillow`

### Arduino sketches

- Arduino IDE
- LoRa library
- TinyGPS++ library
- SoftwareSerial library

## Setup

### 1. Install Python dependencies

The dashboard dependencies are listed in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 2. Upload the Arduino sketches

- Upload `Transmitter.ino` to the GPS-equipped Arduino.
- Upload `Receiver.ino` to the receiving Arduino connected to the PC.
- Make sure both LoRa modules use the same frequency and wiring.

### 3. Update the serial port in the dashboard

In `DashBoard/dynamicdashboard.py`, replace `Enter_Port` with the correct serial port for your receiver board. In `DashBoard/final_dashborad.py`, the port is currently set to `COM3`.

### 4. Run the dashboard

```bash
python DashBoard/dynamicdashboard.py
```

or

```bash
python DashBoard/final_dashborad.py
```

## Using the Dashboard

- Use **Zoom In**, **Zoom Out**, and **Reset Map** to control the map view.
- In `dynamicdashboard.py`, click **Add Boundary Point** and then click on the map to define a custom boundary.
- Click **Confirm Boundary** after placing at least three points.
- Click **Reset Boundary** to clear the current polygon.
- Click **ID** to open the ID generator window.

## Notes

- The dashboard expects incoming serial data in `latitude,longitude` format.
- The system currently uses a Google satellite tile server in the map view.
- If the receiver board is not detected, the dashboard will show a GPS connection error.

## License

No license file is currently included. Add one if you plan to distribute or publish the project.
