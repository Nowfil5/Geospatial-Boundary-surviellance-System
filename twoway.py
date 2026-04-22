import serial
import threading
from tkinter import *
import tkintermapview
from shapely.geometry import Point, Polygon
from tkinter import messagebox

class MaritimeTrackingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maritime Boundary Tracking")
        self.root.geometry("1400x768")
        self.root.configure(bg="#1b263b")
        self.dark_mode = True
        
        # Default maritime boundary coordinates
        self.all_boundary_coords = []  # Stores confirmed boundary
        self.new_boundary_coords = []  # Stores temporary boundary points before confirmation
        self.boundary_polygon = None  # Will be created after confirmation
        
        # Initialize serial connection
        self.serial_port = "COM7"  # Change based on your system
        self.baud_rate = 115200
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        except serial.SerialException as e:
            messagebox.showerror("Error", f"Unable to connect to GPS module: {e}")
            self.ser = None  # Set to None if serial connection fails
        
        self.setup_ui()
        
        # Start GPS reading thread only if serial connection is successful
        if self.ser:
            self.gps_thread = threading.Thread(target=self.read_gps, daemon=True)
            self.gps_thread.start()
    
    def setup_ui(self):
        # UI setup code (same as before)
        pass
    
    def read_gps(self):
        while self.ser and self.ser.is_open:
            try:
                self.ser.reset_input_buffer()  # Clear the serial buffer
                line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                print("Received GPS Data:", line)  # Debugging statement
                if line and "," in line:
                    try:
                        parts = line.split(",")
                        lat, lon = float(parts[0]), float(parts[1])
                        self.update_map(lat, lon)
                    except (ValueError, IndexError) as e:
                        print("Error parsing GPS data:", e)
            except Exception as e:
                print("Error reading GPS data:", e)
                break
    
    def update_map(self, lat, lon):
        marker_color = "green" if self.is_inside_boundary(lat, lon) else "red"
        self.map_widget.set_marker(lat, lon, text=f"Lat: {lat:.4f}, Lon: {lon:.4f}", marker_color_circle=marker_color)
        self.status_bar.config(text=f"Boat Position: {lat:.4f}, {lon:.4f} ({'SAFE' if marker_color == 'green' else 'ALERT!'})")
        
        if marker_color == "red":
            warning_message = f"ALERT! Boat out of boundary: {lat:.4f}, {lon:.4f}"
            if self.ser and self.ser.is_open:
                self.ser.write(warning_message.encode('utf-8'))

if __name__ == "__main__":
    root = Tk()
    app = MaritimeTrackingApp(root)
    root.mainloop()