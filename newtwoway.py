import serial
import threading
from tkinter import *
import tkintermapview
from shapely.geometry import Point, Polygon
from tkinter import messagebox
from PIL import Image, ImageTk
from id_generator import IDGeneratorApp
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
        
        self.setup_ui()
        
        # Start GPS reading thread
        self.gps_thread = threading.Thread(target=self.read_gps, daemon=True)
        self.gps_thread.start()
    
    def setup_ui(self):
        self.left_frame = Frame(self.root, width=300, bg="#0d1b2a", relief=RIDGE, bd=2)
        self.left_frame.pack(side=LEFT, fill=Y, padx=10, pady=10)
        
        Label(self.left_frame, text="Boat Tracking", bg="#0d1b2a", fg="white", font=("Arial", 16, "bold")).pack(pady=20)
        
        Button(self.left_frame, text="Zoom In", command=self.zoom_in, bg="#415a77", fg="white", font=("Arial", 12), width=12).pack(pady=5)
        Button(self.left_frame, text="Zoom Out", command=self.zoom_out, bg="#415a77", fg="white", font=("Arial", 12), width=12).pack(pady=5)
        Button(self.left_frame, text="Reset Map", command=self.reset_position, bg="#778da9", fg="white", font=("Arial", 12), width=12).pack(pady=5)
        Button(self.left_frame, text="Add Boundary Point", command=self.activate_add_boundary_mode, bg="#415a77", fg="white", font=("Arial", 12), width=18).pack(pady=5)
        Button(self.left_frame, text="Confirm Boundary", command=self.confirm_boundary, bg="#4CAF50", fg="white", font=("Arial", 12), width=18).pack(pady=5)
        Button(self.left_frame, text="Reset Boundary", command=self.reset_boundary, bg="#f44336", fg="white", font=("Arial", 12), width=18).pack(pady=5)
        Button(self.left_frame, text="ID", command=self.open_id_generator, bg="#415a77", fg="white", font=("Arial", 12), width=12).pack(side=BOTTOM, pady=10)

        self.status_bar = Label(self.root, text="Awaiting GPS Data...", bg="#0d1b2a", fg="white", font=("Arial", 12), relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.map_widget = tkintermapview.TkinterMapView(self.root, width=850, height=700)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.map_widget.set_position(9, 80)
        self.map_widget.set_zoom(7)
        
        if len(self.all_boundary_coords) >= 2:
            self.map_widget.set_path(self.all_boundary_coords)

        self.map_widget.add_left_click_map_command(self.add_boundary_point)
        self.add_boundary_mode = False
    
    def activate_add_boundary_mode(self):
        self.add_boundary_mode = True
        self.status_bar.config(text="Click on the map to add a new boundary point.")
    
    def add_boundary_point(self, coordinate):
        lat, lon = coordinate
        if self.add_boundary_mode:
            self.new_boundary_coords.append((lat, lon))
            self.map_widget.set_path(self.new_boundary_coords, width=2, color="blue")
            self.status_bar.config(text=f"New boundary point added at: {lat:.4f}, {lon:.4f}")
            self.add_boundary_mode = False
    
    def confirm_boundary(self):
        if len(self.new_boundary_coords) < 3:
            messagebox.showwarning("Warning", "A boundary must have at least 3 points.")
            return
        
        self.all_boundary_coords = self.new_boundary_coords.copy()
        self.boundary_polygon = Polygon(self.all_boundary_coords)
        self.map_widget.set_path(self.all_boundary_coords, width=2, color="red")
        self.status_bar.config(text="Boundary confirmed.")
        self.send_boundary_to_receiver()
    
    def reset_boundary(self):
        self.all_boundary_coords.clear()
        self.new_boundary_coords.clear()
        self.boundary_polygon = None
        self.map_widget.delete_all_path()
        self.status_bar.config(text="Boundary reset.")
    
    def is_inside_boundary(self, lat, lon):
        if self.boundary_polygon:
            return self.boundary_polygon.contains(Point(lat, lon))
        return False
    def send_boundary_to_receiver(self):
        try:
            ser = serial.Serial("COM7", 115200, timeout=1)  # Change COMx to your receiver port
            boundary_str = ";".join([f"{lat},{lon}" for lat, lon in self.all_boundary_coords])
            ser.write(boundary_str.encode() + b"\n")
            ser.close()
            self.status_bar.config(text="Boundary sent to receiver via serial.")
        except serial.SerialException:
            messagebox.showerror("Error", "Failed to send boundary to receiver.")
    
    def zoom_in(self):
        self.map_widget.set_zoom(self.map_widget.zoom + 1)

    def zoom_out(self):
        self.map_widget.set_zoom(self.map_widget.zoom - 1)
    
    def reset_position(self):
        self.map_widget.set_position(9, 80)
        self.map_widget.set_zoom(7)
    
    def read_gps(self):
        serial_port = "COM7"  # Change based on your system
        baud_rate = 115200
        try:
            ser = serial.Serial(serial_port, baud_rate, timeout=1)
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                print(line)
                if line and "," in line:
                    try:
                        parts = line.split(",")
                        lat, lon = float(parts[0]), float(parts[1])
                        self.update_map(lat, lon)
                    except (ValueError, IndexError):
                        continue
        except serial.SerialException:
            messagebox.showerror("Error", "Unable to connect to GPS module.")
    def open_id_generator(self):
        new_window = Toplevel(self.root)
        IDGeneratorApp(new_window)
    
    def update_map(self, lat, lon):
        marker_color = "green" if self.is_inside_boundary(lat, lon) else "red"
        self.map_widget.set_marker(lat, lon, text=f"Lat: {lat:.4f}, Lon: {lon:.4f}", marker_color_circle=marker_color)
        self.status_bar.config(text=f"Boat Position: {lat:.4f}, {lon:.4f} ({'SAFE' if marker_color == 'green' else 'ALERT!'})")
    
if __name__ == "__main__":
    root = Tk()
    app = MaritimeTrackingApp(root)
    root.mainloop()
