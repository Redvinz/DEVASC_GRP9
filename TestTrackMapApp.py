import unittest
import tkinter as tk
from tkinter import ttk
import TrackMap  # Import the main application class

class TestTrackMapApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = TrackMap(self.root)

    def test_geocoding_valid_location(self):
        # Test geocoding with valid locations
        self.app.start_location.insert(0, "Manila, Philippines")
        self.app.dest_location.insert(0, "Quezon City, Philippines")
        
        self.app.geocoding()



        # Check if coordinates are populated
        start_coords = self.app.start_coords.get()
        dest_coords = self.app.dest_coords.get()
        
        self.assertNotEqual(start_coords, "")
        self.assertNotEqual(dest_coords, "")

    def test_vehicle_selection(self):
        # Test vehicle profile selection
        vehicle_options = ["car", "bike", "foot"]
        for vehicle in vehicle_options:
            self.app.vehicle.set(vehicle)
            self.assertEqual(self.app.vehicle.get(), vehicle)

    def test_reset_functionality(self):
        # Populate fields
        self.app.start_location.insert(0, "Test Start")
        self.app.dest_location.insert(0, "Test Destination")
        
        self.app.reset()
        
        # Check if fields are cleared
        self.assertEqual(self.app.start_location.get(), "")
        self.assertEqual(self.app.dest_location.get(), "")
        self.assertEqual(self.app.vehicle.get(), "car")

    def test_route_calculation(self):
        # Test route calculation with valid locations
        self.app.start_location.insert(0, "Manila, Philippines")
        self.app.dest_location.insert(0, "Quezon City, Philippines")
        
        self.app.geocoding()
        
        # Check if distance and time are calculated
        distance = self.app.distance.cget("text")
        time = self.app.time.cget("text")
        
        self.assertNotEqual(distance, "")
        self.assertNotEqual(time, "")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()