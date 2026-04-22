
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
        
        # Maritime boundary coordinates
        self.all_boundary_coords = [
            (13.6309, 80.2003), (13.3882, 80.2841), (13.2599, 80.2950), (13.1315, 80.2950),
            (13.0352, 80.2621), (12.8853, 80.2401), (12.7353, 80.2181), (12.5960, 80.1742),
            (12.4080, 80.1083), (12.3385, 79.9984), (12.1345, 79.8666), (11.9841, 79.8116),
            (11.6293, 79.7018), (11.5432, 79.7128), (11.3709, 79.8007), (11.1125, 79.8226),
            (10.3135, 79.8226), (10.3351, 79.3063), (9.5189, 78.8454), (9.3151, 78.7904),
            (9.0114, 78.2247), (8.7455, 78.1313), (8.5337, 78.1313), (8.2674, 77.7962),
            (8.1378, 77.5653), (7.3500, 78.6474), (7.5883, 78.7617), (8.2033, 78.8958),
            (8.3700, 78.9233), (8.5200, 79.0783), (8.6200, 79.2167), (8.6667, 79.3033),
            (8.8833, 79.4883), (9.0000, 79.5217), (9.1000, 79.5333), (9.1500, 79.5333),
            (9.3812, 79.4437), (9.6142, 79.4669), (9.8700, 79.5572), (9.9850, 79.7159),
            (10.0424, 79.8871), (10.0833, 80.0500), (10.0967, 80.0833), (10.1400, 80.1583),
            (10.5500, 80.7667), (10.6950, 81.0117), (11.0450, 81.9333), (11.2667, 82.4067),
            (11.4433, 83.3667), (11.8936, 82.9936), (12.2159, 82.5047), (12.6216, 81.9003),
            (13.0140, 81.2185), (13.6309, 80.2003)
        ]
        self.boundary_polygon = Polygon(self.all_boundary_coords)
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
        Button(self.left_frame, text="Light Mode", command=self.toggle_theme, bg="#415a77", fg="white", font=("Arial", 12), width=12).pack(pady=5)
        Button(self.left_frame, text="ID", command=self.open_id_generator, bg="#415a77", fg="white", font=("Arial", 12), width=12).pack(side=BOTTOM, pady=10)

        self.status_bar = Label(self.root, text="Awaiting GPS Data...", bg="#0d1b2a", fg="white", font=("Arial", 12), relief=SUNKEN, anchor=W)
        self.status_bar.pack(side=BOTTOM, fill=X)

        self.map_widget = tkintermapview.TkinterMapView(self.root, width=850, height=700)
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.map_widget.set_position(9, 80)
        self.map_widget.set_zoom(7)
        self.map_widget.set_path(self.all_boundary_coords)
        #self.map_widget.add_left_click_map_command(self.on_map_click)

        # Use event binding instead of the non-existing right-click method
        #self.map_widget.canvas.bind("<Button-3>", self.on_boundary_click)  
    
    def is_inside_boundary(self, lat, lon):
        return self.boundary_polygon.contains(Point(lon, lat))
    def zoom_in(self):
        self.map_widget.set_zoom(self.map_widget.zoom + 1)

    def zoom_out(self):
        self.map_widget.set_zoom(self.map_widget.zoom - 1)
    
    def reset_position(self):
        self.map_widget.set_position(9, 80)
        self.map_widget.set_zoom(7)
    
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

    def open_id_generator(self):
        new_window = Toplevel(self.root)
        IDGeneratorApp(new_window)
    
    def read_gps(self):
        serial_port = "Enter_Port_Name"  # Change based on your system
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
    
    def update_map(self, lat, lon):
        marker_color = "green" if self.is_inside_boundary(lat, lon) else "red"
        self.map_widget.set_marker(lat, lon, text=f"Lat: {lat:.4f}, Lon: {lon:.4f}", marker_color_circle=marker_color)
        if marker_color == "red":
            #print("Warning", f"Boat has crossed the boundary!\nLatitude: {lat}\nLongitude: {lon}")
            self.status_bar.config(text=f"Boat Position: {lat:.4f}, {lon:.4f} ({'SAFE' if marker_color == 'green' else 'ALERT!'})")
    
if __name__ == "__main__":
    root = Tk()
    app = MaritimeTrackingApp(root)
    root.mainloop()
