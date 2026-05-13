class ClassName:

    def __init__(self):
        # this runs automatically when you create an object
        # this is where you define properties
        pass

    def method_name(self):
        # this is something the object can do
        pass


# ============================================================
# DAY 4 — OBJECT ORIENTED PROGRAMMING FROM ZERO
# ============================================================

# ── CONCEPT 1: YOUR FIRST CLASS ─────────────────────────────

# A class is a blueprint
# Like a blueprint for building a house
# The blueprint itself is not a house
# But you can build many houses from it

class Sensors:
    def __init__(self, name, max_range):
        # __init__ runs automatically when you create a sensor
        # These are the properties every sensor has
        self.name = name  # what the sensor is called
        self.max_range = max_range # how far it can detect in metres
        self.is_active = True   # starts as active by default
        self.readings = []  # empty list to store readings
        pass

    def get_info(self):
        # This method prints the sensor information
        print(f"Sensor :{self.name}")
        print(f"Range :{self.max_range} meters")
        print(f"Active :{self.is_active}")
        print(f"Readings :{len(self.readings)}") 
        pass
    
    def add_reading(self , value):
        # This method adds one reading to the list
        self.readings.append(value)
        print(f"{self.name} Recoeded:{value} meters")
        pass

    def get_average(self):
        # This method calculate average of all readings
        if len(self.readings) ==0:
            return 0
        return sum(self.readings) / len(self.readings)
        pass
    
    def deactivate(self):
        # This method turns the sensor off
        self.is_active = False
        print(f"{self.name} has been deactivated")
        pass
# â”€â”€ CREATE OBJECTS FROM THE CLASS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€

# This is called instantiation
# You are creating actual sensors from the blueprint
# ── CREATE OBJECTS FROM THE CLASS ───────────────────────────

# This is called instantiation
# You are creating actual sensors from the blueprint
camera = Sensors("Camera_Front",250)
radar = Sensors("Radar_Front", 200)
lidar = Sensors("Lidar_Top", 150)
ultrasonic = Sensors("ULTRASONIC_REAR", 8)

# Each is a separate objects with its own data
print("=== Sensor Information ===")
camera.get_info()
print()
radar.get_info()
print()
lidar.get_info()
print()
ultrasonic.get_info()

# ── CONCEPT 2: USING METHODS ─────────────────────────────────

print("\n=== Adding Sensors Readings ===")

# Add some distance readings to the radar
radar.add_reading(45.2)
radar.add_reading(43.8)
radar.add_reading(41.5)
radar.add_reading(39.1)
radar.add_reading(36.7)

camera.add_reading(28.5)
camera.add_reading(31.2)
camera.add_reading(27.8)


# Check the average
average_r = radar.get_average()
print(f"\nRadar average distance: {average_r:.2f} meters")

average_c = camera.get_average()
print(f"\nCamera average distance: {average_c:.2f} meters")

#deavtivate the sensor
radar.deactivate()
camera.deactivate()

#check the status changed
print(f"\n Radar active status:{radar.is_active}")
print(f"\n Camera Active status:{camera.is_active}")


# ── CONCEPT 4: A MORE COMPLETE CLASS ────────────────────────

class Camera:

    def __init__(self, name, resolution_width, resolution_height, fps):
        # properties stored wheb camera is created
        self.name = name
        self.resolution_width = resolution_width
        self.resolution_height = resolution_height
        self.fps = fps
        self.is_active = False
        self.frames_captured = 0
        self.total_pixels = resolution_width * resolution_height
        pass

    def turn_on(self):
        self.is_active = True
        print(f"{self.name} Turned ON")
        pass

    def turn_of(self):
        self.is_active = False
        print(f"{self.name} Turned OFF ")
        pass

    def capture_frame(self):
        if self.is_active == False:
            print(f"{self.name} is OFF - cannot capture frame")
            return None
        
        self.frames_captured += 1
        print(f"{self.name} Captured Frame {self.capture_frame}")
        return self.capture_frame
        pass

    def get_status(self):
        status = "ON" if self.is_active else "OFF"
        print(f"---{self.name} status ---")
        print(f"status :{status}")
        print(f"Resolution : {self.resolution_width}x{self.resolution_height}")
        print(f"FPS : {self.fps}")
        print(f"Total Pixels : {self.total_pixels:,}")
        print(f"Frames Captured : {self.frames_captured}")
        pass

    def get_data_rate_mbps(self):
        # Calculate how much data this camera produces per second
        # Each pixel = 3 bytes (RGB)
        # Megabytes per second = pixels * 3 bytes * fps / 1,000,000
        bytes_per_second = self.total_pixels * 3 * self.fps
        mbps = bytes_per_second / 1_000_000
        return mbps
        pass

# create two cameras
front_camera = Camera("Camera_Front", 1280, 720, 30)
rear_camera = Camera("Camera_Rear", 1920, 1080, 60)

print("\n=== Camera System ===")
front_camera.get_status()
print()
rear_camera.get_status()

# ── TASK 3: FRAMES CAPTURED AND DATA RATE ────────────────────

print("\n=== Task 3: Camera Frame Capture Test ===")

# ── PART 1: Try capturing WITHOUT turning on first ───────────
# front_camera.is_active is False by default when created
# The capture_frame() method checks this
# It will print "is OFF — cannot capture frame" and return None
print("\n--- Part 1: Capture without turning on ---")
result = front_camera.capture_frame()

# result will be None because camera is off
# Let us confirm that
print(f"Result returned: {result}")
# This prints: Result returned: None


# ── PART 2: Turn on the camera ───────────────────────────────
# Now we properly turn the camera on
# turn_on() sets self.is_active = True
print("\n--- Part 2: Turn camera ON ---")
front_camera.turn_on()

# Verify it is on by checking the property directly
print(f"Camera active status: {front_camera.is_active}")
# This prints: Camera active status: True


# ── PART 3: Capture 3 frames ─────────────────────────────────
# Now camera is on so capture_frame() will work
# Each call increases self.frames_captured by 1 inside the method
print("\n--- Part 3: Capturing 3 frames ---")
front_camera.capture_frame()
front_camera.capture_frame()
front_camera.capture_frame()

# ── PART 4: Print how many frames were captured ──────────────
print("\n--- Part 4: Frames captured ---")
print(f"Frames captured: {front_camera.frames_captured}")

# ── PART 5: Calculate the data rate ─────────────────────────
# get_data_rate_mbps() is a method in the Camera class
# It calculates: total_pixels * 3 bytes * fps / 1,000,000
# For 1280x720 at 30fps:
#   pixels = 1280 * 720 = 921,600
#   bytes per second = 921,600 * 3 * 30 = 82,944,000
#   MB per second = 82,944,000 / 1,000,000 = 82.944
print("\n--- Part 5: Data rate calculation ---")
data_rate = front_camera.get_data_rate_mbps()

print(f"Resolution      : {front_camera.resolution_width}"
      f"x{front_camera.resolution_height}")
print(f"Total pixels    : {front_camera.total_pixels:,}")
print(f"FPS             : {front_camera.fps}")
print(f"Bytes per second: "
      f"{front_camera.total_pixels * 3 * front_camera.fps:,}")
print(f"Data rate       : {data_rate:.3f} MB/s")


# ── PART 6: Printing the final sentence ────────────────────────
# Use the data_rate variable we stored in Part 5
print("\n--- Part 6: Final sentence ---")
print(f"Front camera produces {data_rate:.3f} MB of data per second")

# ── CONCEPT 5: INHERITANCE ───────────────────────────────────

# This is the PARENT class (also called base class)
# It has the common things ALL sensors share
class SensorBase:
    def __init__(self, name, sensor_type, max_range):
        self.name  = name
        self.sensor_type  =  sensor_type
        self.max_range  =  max_range
        self.is_active  =  True
        self.error_count  =  0 
        pass

    def activate(self):
        self.is_active = True
        print(f"{self.name} Ativated")

    def deactivate(self):
        self.is_active = False
        print(f"{self.name} Deactivated")

    def error_report(self):
        self.error_count += 1
        print(f"{self.name} Error #{self.error_count}")

    def get_basic_Info(self):
        print(f"Name : {self.name}")
        print(f"Type : {self.sensor_type}")
        print(f"Range : {self.max_range}m")
        print(f"Active : {self.is_active}")
        print(f"Errors : {self.error_count}")

# This is a CHILD class (also called derived class)
# It inherits everything from SensorBase
# AND adds its own LiDAR-specific things
class LidarSensor(SensorBase):    # <-- SensorBase in brackets means inherit

    def __init__(self, name, max_range, num_beams, rotation_rate_hz):
         # super().__init__() calls the parent __init__
        # This sets up all the basic sensor properties
        super().__init__(name, "LiDAR", max_range)

        # now add LiDAR specific properties
        self.num_beams = num_beams
        self.rotation_rate_hz = rotation_rate_hz
        self.points_per_scan = 0

    def scan(self):
        if not self.is_active:
            print(f"{self.name} is OFF — cannot scan")
            return
        # Each scan produces points based on beams
        self.points_per_scan = self.num_beams * 1024
        print(f"{self.name} scanned: {self.points_per_scan:,} points")
    
    def get_full_info(self):
        # First call parent method to show basic info
        self.get_basic_Info()
        # Then show LiDAR specific info
        print(f"Beams  : {self.num_beams}")
        print(f"Spin   : {self.rotation_rate_hz} Hz")
        print(f"Points : {self.points_per_scan:,}")


# Another child class for radar
class RadarSensor(SensorBase):
    
    def __init__(self, name, max_range, frequency_ghz):
        super().__init__(name, "Radar", max_range)
        self.frequency_ghz = frequency_ghz
        self.detected_objects = []
    
    def detect(self, distance, velocity):
        if not self.is_active:
            print(f"{self.name} is OFF")
            return
        obj = {"distance": distance, "velocity": velocity}
        self.detected_objects.append(obj)
        print(f"{self.name} detected: {distance}m at {velocity}m/s")
    
    def get_full_info(self):
        self.get_basic_Info()
        print(f"Freq   : {self.frequency_ghz} GHz")
        print(f"Objects: {len(self.detected_objects)}")


# Create objects from child classes
velodyne = LidarSensor("VELODYNE_HDL64", 150, 64, 10)
bosch_radar = RadarSensor("BOSCH_LRR4", 250, 77.0)

print("\n=== LiDAR Sensor ===")
velodyne.get_full_info()

print()
velodyne.scan()
velodyne.scan()
velodyne.scan()

print(f"\nAfter 3 scans: {velodyne.points_per_scan:,} points per scan")

print("\n=== Radar Sensor ===")
bosch_radar.get_full_info()
bosch_radar.detect(45.2, 12.5)
bosch_radar.detect(28.7, 8.3)
bosch_radar.detect(15.1, 20.1)
# ── CONCEPT 6: ADAS SENSOR MANAGER ──────────────────────────

class ADASSensorManager:
    
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.sensors    = {}    # dictionary: name -> sensor object
        print(f"Sensor Manager created for vehicle: {vehicle_id}")
    
    def add_sensor(self, sensor):
        # Add a sensor to the manager
        # sensor.name is used as the key
        self.sensors[sensor.name] = sensor
        print(f"Added sensor: {sensor.name}")
    
    def activate_all(self):
        print("\nActivating all sensors...")
        for name, sensor in self.sensors.items():
            sensor.activate()
    
    def deactivate_all(self):
        print("\nDeactivating all sensors...")
        for name, sensor in self.sensors.items():
            sensor.deactivate()
    
    def get_active_count(self):
        count = 0
        for name, sensor in self.sensors.items():
            if sensor.is_active:
                count += 1
        return count
    
    def system_health_check(self):
        print(f"\n=== System Health Check — Vehicle {self.vehicle_id} ===")
        print(f"Total sensors  : {len(self.sensors)}")
        print(f"Active sensors : {self.get_active_count()}")
        print(f"Offline sensors: {len(self.sensors) - self.get_active_count()}")
        print()
        for name, sensor in self.sensors.items():
            status = "OK" if sensor.is_active else "OFFLINE"
            errors = sensor.error_count
            flag   = "  " if errors == 0 else "!!"
            print(f"  {flag} {name:25s} | {status:7s} | Errors: {errors}")


# Create the manager
manager = ADASSensorManager("VEHICLE_001")

# Create sensors (reusing classes from above)
s1 = LidarSensor("LIDAR_TOP",    150, 64, 10)
s2 = RadarSensor("RADAR_FRONT",  250, 77.0)
s3 = RadarSensor("RADAR_REAR",   100, 77.0)
s4 = SensorBase("ULTRASONIC_FL", "Ultrasonic", 8)
s5 = SensorBase("ULTRASONIC_FR", "Ultrasonic", 8)

# Add all to manager
print()
manager.add_sensor(s1)
manager.add_sensor(s2)
manager.add_sensor(s3)
manager.add_sensor(s4)
manager.add_sensor(s5)

# Health check — all should be active
manager.system_health_check()

# Simulate some errors and deactivation
s3.report_error()
s3.report_error()
s4.deactivate()

# Health check again — should show changes
manager.system_health_check()



