import tkinter as tk
from tkinter import ttk

class TrackMapApp:
    def __init__(self, master):
        self.master = master
        master.title("TrackMap")
        master.geometry("350x550")

        # triny ko kaso yung border lang 
        style = ttk.Style()
        style.configure("Black.TButton", foreground="white", background="black")

        # title
        ttk.Label(master, text="TrackMap", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(master, text="GraphHopper Pro", font=("Arial", 10)).pack()

        # vehicles
        ttk.Label(master, text="Enter a vehicle profile from the list:").pack(anchor="w", padx=10, pady=(10, 0))
        
        self.vehicle = tk.StringVar(value="car")
        ttk.Radiobutton(master, text="Car\nFastest travel by road", variable=self.vehicle, value="car").pack(anchor="w", padx=20)
        ttk.Radiobutton(master, text="Bike\nEco-friendly, slower than car.", variable=self.vehicle, value="bike").pack(anchor="w", padx=20)
        ttk.Radiobutton(master, text="Foot\nWalking, best for short distances.", variable=self.vehicle, value="foot").pack(anchor="w", padx=20)

        # starting loc
        ttk.Label(master, text="Starting Location:").pack(anchor="w", padx=10, pady=(10, 0))
        self.start_location = ttk.Entry(master)
        self.start_location.pack(fill="x", padx=10)

        # destination
        ttk.Label(master, text="Destination:").pack(anchor="w", padx=10, pady=(10, 0))
        self.destination = ttk.Entry(master)
        self.destination.pack(fill="x", padx=10)

        # go button (di ko medyo maconfig yung color)
        ttk.Button(master, text="Go", command=self.geocoding, style="Black.TButton").pack(fill="x", padx=10, pady=10)

        # distance and time
        frame = ttk.Frame(master)
        frame.pack(fill="x", padx=10)

        ttk.Label(frame, text="Distance:").grid(row=0, column=0, sticky="w")
        self.distance = ttk.Entry(frame, width=10)
        self.distance.grid(row=0, column=1, padx=(0, 10))
        self.distance.insert(0, "200km")

        ttk.Label(frame, text="Estimated Time of Travel").grid(row=0, column=2, sticky="w")
        self.time = ttk.Entry(frame, width=10)
        self.time.grid(row=0, column=3)
        self.time.insert(0, "200km")

        # directions
        ttk.Label(master, text="Directions:").pack(anchor="w", padx=10, pady=(10, 0))
        self.directions = tk.Text(master, height=5)
        self.directions.pack(fill="x", padx=10)

        # reset button
        ttk.Button(master, text="Go for another travel (RESET)", command=self.reset, style="Black.TButton").pack(fill="x", padx=10, pady=10)

    def geocoding(self):
        # palagay nung mismong method
        pass

    def reset(self):
        # reset  fields
        self.start_location.delete(0, 'end')
        self.destination.delete(0, 'end')
        self.directions.delete('1.0', 'end')
        self.vehicle.set("car")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrackMapApp(root)
    root.mainloop()