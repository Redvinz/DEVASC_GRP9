import tkinter as tk
from tkinter import ttk
import requests
import urllib.parse
import tkintermapview


class TrackMapApp:
    def __init__(self, master):
        self.master = master
        master.title("TrackMap")
        master.geometry("1000x600")
        master.resizable(False, False)
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=1)
        master.rowconfigure(0, weight=1)
        
        # Configure style
        style = ttk.Style()
        style.configure("Black.TButton", foreground="white", background="black")

        frame1 = ttk.Frame(master)
        frame1.grid(row=0, column=0, sticky="ns")
        
        frame2 = ttk.Frame(master)
        frame2.grid(row=0, column=1, sticky="ns")
        # Title
        ttk.Label(frame1, text="TrackMap", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame1, text="GraphHopper Pro", font=("Arial", 10)).pack()

        # Vehicles
        ttk.Label(frame1, text="Enter a vehicle profile from the list:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.vehicle = tk.StringVar(value="car")
        ttk.Radiobutton(
            frame1,
            text="Car\nFastest travel by road",
            variable=self.vehicle,
            value="car",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            frame1,
            text="Bike\nEco-friendly, slower than car.",
            variable=self.vehicle,
            value="bike",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            frame1,
            text="Foot\nWalking, best for short distances.",
            variable=self.vehicle,
            value="foot",
        ).pack(anchor="w", padx=20)

        # Starting Location
        ttk.Label(frame1, text="Starting Location:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.start_location = ttk.Entry(frame1)
        self.start_location.pack(fill="x", padx=10)

        # Start Coordinates
        frame_start = ttk.Frame(frame1)
        frame_start.pack(fill="x", padx=10)

        ttk.Label(frame_start, text="Start (Lat, Long):").grid(row=0, column=0, sticky="w")
        self.start_coords = ttk.Entry(frame_start)
        self.start_coords.grid(row=0, column=1, padx=(0, 10))

        # Destination
        ttk.Label(frame1, text="Destination:").pack(anchor="w", padx=10, pady=(10, 0))
        self.destination = ttk.Entry(frame1)
        self.destination.pack(fill="x", padx=10)

        # Destination Coordinates
        frame_dest = ttk.Frame(frame1)
        frame_dest.pack(fill="x", padx=10)

        ttk.Label(frame_dest, text="Destination (Lat, Long):").grid(row=0, column=0, sticky="w")
        self.dest_coords = ttk.Entry(frame_dest)
        self.dest_coords.grid(row=0, column=1, padx=(0, 10))

        # Go Button
        ttk.Button(
            frame1, text="Go", command=self.geocoding, style="Black.TButton"
        ).pack(fill="x", padx=10, pady=10)

        # Distance and Time
        frame = ttk.Frame(frame1)
        frame.pack(fill="x", padx=10)

        ttk.Label(frame, text="Distance:").grid(row=0, column=0, sticky="w")
        self.distance = ttk.Entry(frame, width=10)
        self.distance.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(frame, text="Estimated Time of Travel").grid(
            row=0, column=2, sticky="w"
        )
        self.time = ttk.Entry(frame, width=10)
        self.time.grid(row=0, column=3)

        # Directions
        ttk.Label(frame1, text="Directions:").pack(anchor="w", padx=10, pady=(10, 0))
        self.directions = tk.Text(frame1, height=5)
        self.directions.pack(fill="x", padx=10)

        # Reset Button
        ttk.Button(
            frame1,
            text="Go for another travel (RESET)",
            command=self.reset,
            style="Black.TButton",
        ).pack(fill="x", padx=10, pady=10)

        # Map
        self.map = tkintermapview.TkinterMapView(frame2, width=550, height=550, corner_radius=10)
        self.map.set_position(14.61012695, 120.9892056708045)
        self.map.pack(fill=tk.BOTH, expand=True)


    def geocoding(self):
        key = "9883cac5-0db3-4446-8507-a59b80acf13d"  # change to other api key
        start_location = self.start_location.get()
        destination = self.destination.get()
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
                        distance_km, time_sec, route_data["instructions"], route_data['path_points']
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
                "path_points" : data["paths"][0]["points"]["coordinates"],
            }
        return None

    def display_route_info(self, distance_km, time_sec, instructions, path_points):
        self.path = self.map.set_path([self.start_marker.position, self.start_marker.position])
        
        for long, lat  in path_points:
            self.path.add_position(lat, long)

        # Update distance and time fields
        self.distance.delete(0, tk.END)
        self.distance.insert(0, f"{distance_km:.2f} km")

        hours = int(time_sec // 3600)
        minutes = int((time_sec % 3600) // 60)
        self.time.delete(0, tk.END)
        self.time.insert(0, f"{hours:02d}:{minutes:02d}")

        # Clear and display directions
        self.directions.delete(1.0, tk.END)
        for instruction in instructions:
            text = instruction["text"]
            self.directions.insert(tk.END, text + "\n")

    def reset(self):
        # Reset fields
        self.start_location.delete(0, "end")
        self.destination.delete(0, "end")
        self.start_coords.delete(0, "end")
        self.dest_coords.delete(0, "end")
        self.directions.delete("1.0", "end")
        self.vehicle.set("car")
        self.map.delete_all_marker()
        self.map.set_position(14.61012695, 120.9892056708045)
        self.path.delete()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrackMapApp(root)
    root.mainloop()