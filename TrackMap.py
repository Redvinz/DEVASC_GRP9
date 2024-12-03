import tkinter as tk
from tkinter import ttk
import requests
import urllib.parse
import tkintermapview


class TrackMapApp:
    def __init__(self, master):
        self.master = master
        master.title("TrackMap")
        master.geometry("1200x850")
        master.resizable(True, True)

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # Create main frames
        self.create_frames()

        # Create widgets
        self.create_widgets()

    def configure_styles(self):
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 10))
        self.style.configure(
            "TRadiobutton", background="#f0f0f0", font=("Helvetica", 10)
        )
        self.style.configure("TEntry", font=("Helvetica", 10))
        self.style.configure("TButton", font=("Helvetica", 10, "bold"))
        self.style.configure(
            "Title.TLabel", font=("Helvetica", 24, "bold"), foreground="#333333"
        )
        self.style.configure(
            "Subtitle.TLabel", font=("Helvetica", 12), foreground="#666666"
        )
        self.style.configure(
            "Section.TLabel", font=("Helvetica", 12, "bold"), foreground="#333333"
        )

    def create_frames(self):
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.left_frame = ttk.Frame(self.main_frame, padding="20")
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_widgets(self):
        # Title and subtitle
        ttk.Label(self.left_frame, text="TrackMap", style="Title.TLabel").pack(
            pady=(0, 5)
        )
        ttk.Label(
            self.left_frame, text="Powered by GraphHopper Pro", style="Subtitle.TLabel"
        ).pack(pady=(0, 20))

        # Vehicle selection
        ttk.Label(self.left_frame, text="Vehicle Profile", style="Section.TLabel").pack(
            anchor="w", pady=(10, 5)
        )
        self.vehicle = tk.StringVar(value="car")
        for value, text in [("car", "Car"), ("bike", "Bike"), ("foot", "Foot")]:
            ttk.Radiobutton(
                self.left_frame, text=text, variable=self.vehicle, value=value
            ).pack(anchor="w", padx=10)

        # Location inputs
        self.create_location_input("Starting Location", self.left_frame, "start")
        self.create_location_input("Destination", self.left_frame, "dest")

        # Go Button
        ttk.Button(
            self.left_frame, text="Find Route", command=self.geocoding, style="TButton"
        ).pack(fill="x", pady=20)

        # Results frame
        self.results_frame = ttk.Frame(self.left_frame)
        self.results_frame.pack(fill="x", pady=10)

        # Distance and Time
        self.create_result_field("Distance:", "distance")
        self.create_result_field("Est. Travel Time:", "time")

        # Directions
        ttk.Label(self.left_frame, text="Directions:", style="Section.TLabel").pack(
            anchor="w", pady=(20, 5)
        )
        self.directions = tk.Text(
            self.left_frame, height=10, width=40, wrap=tk.WORD, font=("Helvetica", 10)
        )
        self.directions.pack(fill="x")

        # Reset Button
        ttk.Button(
            self.left_frame, text="Reset", command=self.reset, style="TButton"
        ).pack(fill="x", pady=0)

        # History Button (button opens a new window)
        ttk.Button(
            self.left_frame,
            text="History",
            command=self.open_history_window,
            style="TButton",
        ).pack(fill="x", pady=5)

        # Map
        self.map = tkintermapview.TkinterMapView(self.right_frame, corner_radius=0)
        self.map.pack(fill=tk.BOTH, expand=True)
        self.map.set_position(14.61012695, 120.9892056708045)  # UST Coordinates

    def create_location_input(self, label, parent, prefix):
        ttk.Label(parent, text=label, style="Section.TLabel").pack(
            anchor="w", pady=(20, 5)
        )
        setattr(self, f"{prefix}_location", ttk.Entry(parent))
        getattr(self, f"{prefix}_location").pack(fill="x")

        coord_frame = ttk.Frame(parent)
        coord_frame.pack(fill="x", pady=(5, 0))
        ttk.Label(coord_frame, text="Lat, Long:").pack(side=tk.LEFT)
        setattr(self, f"{prefix}_coords", ttk.Entry(coord_frame, width=25))
        getattr(self, f"{prefix}_coords").pack(side=tk.LEFT, padx=(5, 0))

    def create_result_field(self, label, attr_name):
        frame = ttk.Frame(self.results_frame)
        frame.pack(fill="x", pady=2)
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        setattr(self, attr_name, ttk.Label(frame, width=15))
        getattr(self, attr_name).pack(side=tk.RIGHT)

    def geocoding(self):
        key = "9883cac5-0db3-4446-8507-a59b80acf13d"  # change to other api key
        start_location = self.start_location.get()
        destination = self.dest_location.get()
        vehicle = self.vehicle.get()

        if start_location and destination:
            orig = self.get_geocoding_data(start_location, key)
            dest = self.get_geocoding_data(destination, key)

            if orig and dest:
                # Display start and destination coordinates
                self.start_coords.delete(0, tk.END)
                self.start_coords.insert(0, f"{orig[0]:.6f}, {orig[1]:.6f}")

                self.dest_coords.delete(0, tk.END)
                self.dest_coords.insert(0, f"{dest[0]:.6f}, {dest[1]:.6f}")

                self.map.set_position(orig[0], orig[1])
                self.start_marker = self.map.set_marker(orig[0], orig[1], text="Start")
                self.finish_marker = self.map.set_marker(dest[0], dest[1], text="End")

                route_data = self.get_route_data(orig, dest, vehicle, key)
                if route_data:
                    distance_km = route_data["distance"] / 1000
                    time_sec = route_data["time"] / 10
                    self.display_route_info(
                        distance_km,
                        time_sec,
                        route_data["instructions"],
                        route_data["path_points"],
                    )

    def get_geocoding_data(self, location, key):
        geocode_url = "https://graphhopper.com/api/1/geocode?"
        url = geocode_url + urllib.parse.urlencode(
            {"q": location, "limit": "1", "key": key}
        )
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data["hits"]:
                point = data["hits"][0]["point"]
                return point["lat"], point["lng"]
        return None

    def get_route_data(self, orig, dest, vehicle, key):
        route_url = "https://graphhopper.com/api/1/route?"
        params = {
            "point": [f"{orig[0]},{orig[1]}", f"{dest[0]},{dest[1]}"],
            "vehicle": vehicle,
            "points_encoded": False,
            "key": key,
        }
        url = route_url + urllib.parse.urlencode(params, doseq=True)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return {
                "distance": data["paths"][0]["distance"],
                "time": data["paths"][0]["time"],
                "instructions": data["paths"][0]["instructions"],
                "path_points": data["paths"][0]["points"]["coordinates"],
            }
        return None

    def display_route_info(self, distance_km, time_sec, instructions, path_points):
        self.path = self.map.set_path(
            [self.start_marker.position, self.start_marker.position]
        )

        for long, lat in path_points:
            self.path.add_position(lat, long)

        # Update distance and time fields
        self.distance.config(text=f"{distance_km:.2f} km")

        hours = int(time_sec // 3600)
        minutes = int((time_sec % 3600) // 60)
        self.time.config(text=f"{hours:02d}:{minutes:02d}")

        # Clear and display directions
        self.directions.delete(1.0, tk.END)
        for instruction in instructions:
            text = instruction["text"]
            self.directions.insert(tk.END, text + "\n")

    def reset(self):
        # Reset fields
        self.start_location.delete(0, "end")
        self.dest_location.delete(0, "end")
        self.start_coords.delete(0, "end")
        self.dest_coords.delete(0, "end")
        self.directions.delete("1.0", "end")
        self.vehicle.set("car")
        self.map.delete_all_marker()
        self.map.set_position(14.61012695, 120.9892056708045)

        # Check if path exists before deleting it
        if hasattr(self, "path") and self.path:
            self.path.delete()

    def open_history_window(self):
        # new Toplevel window
        history_window = tk.Toplevel(self.master)
        history_window.title("History")
        history_window.geometry("600x400")
        history_window.resizable(False, False)

        # add title label
        ttk.Label(history_window, text="Route History", style="Title.TLabel").pack(
            pady=10
        )

        # test treeview
        columns = ("Start Location", "Destination", "Vehicle", "Distance", "Time")
        tree = ttk.Treeview(history_window, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # column headings
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        # dummy data for demonstration. read data off csv file
        demo_data = [
            ("New York", "Los Angeles", "Car", "4500 km", "40:30"),
            ("London", "Paris", "Bike", "344 km", "20:15"),
        ]
        for row in demo_data:
            tree.insert("", "end", values=row)

        # Close button
        ttk.Button(
            history_window,
            text="Close",
            command=history_window.destroy,
            style="TButton",
        ).pack(pady=10)


if __name__ == "__main__":  # checks if script is run directly (not a module)
    root = tk.Tk()  # call Tkinter constructor and assign root window to root
    app = TrackMapApp(root)  # the root is now the parent container for the app
    root.mainloop()  # needed to keep the interface running
