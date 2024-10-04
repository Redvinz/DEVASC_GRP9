import tkinter as tk
from tkinter import ttk
import requests
import urllib.parse


class TrackMapApp:
    def __init__(self, master):
        self.master = master
        master.title("TrackMap")
        master.geometry("350x550")

        # Configure style
        style = ttk.Style()
        style.configure("Black.TButton", foreground="white", background="black")

        # Title
        ttk.Label(master, text="TrackMap", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(master, text="GraphHopper Pro", font=("Arial", 10)).pack()

        # Vehicles
        ttk.Label(master, text="Enter a vehicle profile from the list:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.vehicle = tk.StringVar(value="car")
        ttk.Radiobutton(
            master,
            text="Car\nFastest travel by road",
            variable=self.vehicle,
            value="car",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            master,
            text="Bike\nEco-friendly, slower than car.",
            variable=self.vehicle,
            value="bike",
        ).pack(anchor="w", padx=20)
        ttk.Radiobutton(
            master,
            text="Foot\nWalking, best for short distances.",
            variable=self.vehicle,
            value="foot",
        ).pack(anchor="w", padx=20)

        # Starting Location
        ttk.Label(master, text="Starting Location:").pack(
            anchor="w", padx=10, pady=(10, 0)
        )
        self.start_location = ttk.Entry(master)
        self.start_location.pack(fill="x", padx=10)

        # Destination
        ttk.Label(master, text="Destination:").pack(anchor="w", padx=10, pady=(10, 0))
        self.destination = ttk.Entry(master)
        self.destination.pack(fill="x", padx=10)

        # Go Button
        ttk.Button(
            master, text="Go", command=self.geocoding, style="Black.TButton"
        ).pack(fill="x", padx=10, pady=10)

        # Distance and Time
        frame = ttk.Frame(master)
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
        ttk.Label(master, text="Directions:").pack(anchor="w", padx=10, pady=(10, 0))
        self.directions = tk.Text(master, height=5)
        self.directions.pack(fill="x", padx=10)

        # Reset Button
        ttk.Button(
            master,
            text="Go for another travel (RESET)",
            command=self.reset,
            style="Black.TButton",
        ).pack(fill="x", padx=10, pady=10)

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
