import serial
import tkinter as tk
import tkintermapview
from shapely.geometry import Point, Polygon
from tkinter import messagebox, BOTH
import threading

# Maritime boundary coordinates
all_boundary_coords = [
    (13.6309, 80.2003), (13.3882, 80.2841), (13.2599, 80.2950), (13.1315, 80.2950),
    (13.0352, 80.2621), (12.8853, 80.2401), (12.7353, 80.2181), (12.5960, 80.1742),
    (12.4080, 80.1083), (12.3385, 79.9984), (12.1345, 79.8666), (11.9841, 79.8116),
    (11.6293, 79.7018), (11.5432, 79.7128), (11.3709, 79.8007), (11.1125, 79.8226),
    (10.3135, 79.8226), (10.3351, 79.3063), (9.5189, 78.8454), (9.3151, 78.7904),
    (9.0114, 78.2247), (8.7455, 78.1313), (8.5337, 78.1313), (8.2674, 77.7962),
    (8.1378, 77.5653), (7.3500, 78.6474), (7.5883, 78.7617), (8.2033, 78.8958),
    (8.3700, 78.9233), (8.5200, 79.0783), (8.6200, 79.2167), (8.6667, 79.3033),
    (8.8833, 79.4883), (9.0000, 79.5217), (9.1000, 79.5333), (9.1500, 79.5333)
]

boundary_polygon = Polygon(all_boundary_coords)

def is_inside_boundary(lat, lon):
    return boundary_polygon.contains(Point(lon, lat))

def read_gps():
    serial_port = "COM4"  # Change based on system
    baud_rate = 115200
    
    try:
        ser = serial.Serial(serial_port, baud_rate, timeout=1)
        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(f"Raw Data: {line}")
            if "," in line:  
                try:
                    lat, lon = map(float, line.split(","))
                    update_map(lat, lon)
                    if not is_inside_boundary(lat, lon):
                        ser.write(b"ALERT\n")  # Send alert back to Arduino
                except ValueError:
                    continue
    except serial.SerialException:
        messagebox.showerror("Error", "Unable to connect to GPS module.")

def update_map(lat, lon):
    global map_widget
    marker_color = "green" if is_inside_boundary(lat, lon) else "red"
    map_widget.set_marker(lat, lon, text=f"Lat: {lat:.4f}, Lon: {lon:.4f}", marker_color_circle=marker_color)

map_window = tk.Tk()
map_widget = tkintermapview.TkinterMapView(map_window, width=800, height=600)
map_widget.pack(fill=BOTH, expand=True)
gps_thread = threading.Thread(target=read_gps, daemon=True)
gps_thread.start()
map_window.mainloop()