import tkinter as tk
from tkinter import ttk
import requests
import urllib.parse


class TrackMapApp:
    def __init__(self, master):
        self.master = master
        master.title("TrackMap")
        master.geometry("1000x600")

        # Configure style
        style = ttk.Style()
        style.configure("Black.TButton", foreground="white", background="black")

        # Create main frame
        main_frame = ttk.Frame(master)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create left frame for controls (1/3 width)
        left_frame = ttk.Frame(main_frame, width=400)  # Set a fixed width
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        left_frame.pack_propagate(False)  # Prevent the frame from shrinking

        # Create right frame for map placeholder (2/3 width)
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(left_frame, text="TrackMap", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(left_frame, text="GraphHopper Pro", font=("Arial", 10)).pack()

        # Vehicles
        ttk.Label(left_frame, text="Enter a vehicle profile from the list:").pack(anchor="w", pady=(10, 0))
        self.vehicle = tk.StringVar(value="car")
        ttk.Radiobutton(left_frame, text="Car\nFastest travel by road", variable=self.vehicle, value="car").pack(anchor="w")
        ttk.Radiobutton(left_frame, text="Bike\nEco-friendly, slower than car.", variable=self.vehicle, value="bike").pack(anchor="w")
        ttk.Radiobutton(left_frame, text="Foot\nWalking, best for short distances.", variable=self.vehicle, value="foot").pack(anchor="w")

        # Starting Location
        ttk.Label(left_frame, text="Starting Location:").pack(anchor="w", pady=(10, 0))
        self.start_location = ttk.Entry(left_frame)
        self.start_location.pack(fill="x", padx=5)

        # Destination
        ttk.Label(left_frame, text="Destination:").pack(anchor="w", pady=(10, 0))
        self.destination = ttk.Entry(left_frame)
        self.destination.pack(fill="x", padx=5)

        # Go Button
        ttk.Button(left_frame, text="Go", command=self.geocoding, style="Black.TButton").pack(fill="x", pady=10, padx=5)

        # Distance and Time
        frame = ttk.Frame(left_frame)
        frame.pack(fill="x", padx=5)

        ttk.Label(frame, text="Distance:").grid(row=0, column=0, sticky="w")
        self.distance = ttk.Entry(frame, width=10)
        self.distance.grid(row=0, column=1, padx=(0, 10))

        ttk.Label(frame, text="Estimated Time of Travel").grid(row=0, column=2, sticky="w")
        self.time = ttk.Entry(frame, width=10)
        self.time.grid(row=0, column=3)

        # Directions
        ttk.Label(left_frame, text="Directions:").pack(anchor="w", pady=(10, 0))
        self.directions = tk.Text(left_frame, height=5)
        self.directions.pack(fill="both", expand=True, padx=5)

        # Reset Button
        ttk.Button(left_frame, text="Go for another travel (RESET)", command=self.reset, style="Black.TButton").pack(fill="x", pady=10, padx=5)

        # Map placeholder
        self.map_placeholder = tk.Canvas(right_frame, bg="lightgray")
        self.map_placeholder.pack(fill=tk.BOTH, expand=True)
        self.map_placeholder.create_text(300, 300, text="Map Placeholder (2/3 width)", font=("Arial", 20))

    def geocoding(self):
        key = "9883cac5-0db3-4446-8507-a59b80acf13d"  # change to other api key
        start_location = self.start_location.get()
        destination = self.destination.get()
        vehicle = self.vehicle.get()

        if start_location and destination:
            orig = self.get_geocoding_data(start_location, key)
            dest = self.get_geocoding_data(destination, key)

            if orig and dest:
                route_data = self.get_route_data(orig, dest, vehicle, key)
                if route_data:
                    distance_km = route_data["distance"] / 1000
                    time_sec = route_data["time"] / 1000
                    self.display_route_info(
                        distance_km, time_sec, route_data["instructions"]
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
            }
        return None

    def display_route_info(self, distance_km, time_sec, instructions):
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
        self.directions.delete("1.0", "end")
        self.vehicle.set("car")


if __name__ == "__main__":
    root = tk.Tk()
    app = TrackMapApp(root)
    root.mainloop()
