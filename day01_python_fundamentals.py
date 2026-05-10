# ============================================================
# DAY 1 — PYTHON FUNDAMENTALS FOR ADAS ENGINEERING
# Every concept here will be used in your ADAS projects
# ============================================================

# ── VARIABLES AND DATA TYPES ──────────────────────────────

# Integer — used for: frame numbers, class IDs, pixel coordinates
frame_number = 0
object_class_id = 2          # 2 = Car in KITTI dataset
pixel_x = 640                # x coordinate of detected object

# Float — used for: confidence scores, distances, probabilities
confidence_score = 0.87      # YOLOv8 detection confidence (0 to 1)
distance_meters = 23.5       # distance to vehicle ahead (for AEB)AEB = autonomous emergency braking
time_to_collision = 1.8      # TTC in seconds (critical for AEB trigger)

# String — used for: sensor names, class labels, file paths
sensor_name = "CAMERA_FRONT"
object_class = "Car"
dataset_path = "/home/user/adas-workspace/datasets/kitti/"

# Boolean — used for: flags, detection results, system states
aeb_activated = False        # is automatic emergency braking on?
lane_departure_detected = True # vehicle is moving out of lane
camera_healthy = True

# None — used for: missing sensor data, uninitialised objects
lidar_reading = None         # LiDAR not yet calibrated

# Print all values with context
print("=== ADAS System Status ===")
print(f"Frame: {frame_number}")
print(f"Detected: {object_class} with confidence {confidence_score:.2f}")
print(f"Distance: {distance_meters}m | TTC: {time_to_collision}s")
print(f"AEB Active: {aeb_activated}")
print(f"Lane Departure: {lane_departure_detected}")
print(f"Camera: {'OK' if camera_healthy else 'FAULT'}")

# ── LISTS — STORING MULTIPLE DETECTIONS ──────────────────

# In ADAS, every frame has multiple detected objects
# We store them in lists

# Empty list — starts with no detections
detections = []

# List of detected class names in one frame
detected_classes = ["Car", "Car", "Pedestrian", "Cyclist", "Car"]

# List of confidence scores matching each detection
confidences = [0.92, 0.87, 0.76, 0.83, 0.91]

# List of distances from LiDAR (metres)
distances = [15.3, 28.7, 8.2, 12.1, 45.6]

# ── ACCESSING LIST ELEMENTS ──────────────────────────────
print("\n=== Detection Analysis ===")
print(f"First detection: {detected_classes[0]}")    # index 0 = first. output will be Car
print(f"Last detection: {detected_classes[-1]}")    # -1 = last. output will be Car 
print(f"Second and third: {detected_classes[1:3]}") # slicing. output will be 1st position Car & 2nd Pedestrian

# ── LIST OPERATIONS ───────────────────────────────────────
print(f"Total detections: {len(detected_classes)}")
print(f"Number of cars: {detected_classes.count('Car')}")
print(f"Closest object: {min(distances)}m")
print(f"Farthest object: {max(distances)}m")

# Add a new detection
detected_classes.append("Truck")
confidences.append(0.79)
distances.append(32.4)
print(f"After adding truck the: {len(detected_classes)} object") 

# ── LOOPING THROUGH DETECTIONS ────────────────────────────
print("\n=== All Detections ===")
for i in range(len(detected_classes)):
    print(f"  {i+1}. {detected_classes[i]:12s} | "
          f"Confidence: {confidences[i]:.2f} | "
          f"Distance: {distances[i]:5.1f}m")

# ── LIST COMPREHENSION — FILTER DETECTIONS ────────────────
# Get only high-confidence detections (confidence > 0.80)
# This is exactly what NMS (Non-Maximum Suppression) does in YOLO
high_conf_indices = [i for i in range(len(confidences))
                     if confidences[i] > 0.80]

print(f"\n THe High confidence detections (>0.80) is: {len(high_conf_indices)}")

# Get distances of only high-confidence objects
high_conf_distances = [distances[i] for i in high_conf_indices]
print(f"Their distances is: {high_conf_distances}")

# Filter objects closer than 20m (danger zone for AEB)
danger_zone = [(detected_classes[i], distances[i])
               for i in range(len(distances))
               if distances[i] < 20.0]
print(f"\nObjects in danger zone (<20m): {danger_zone}")

# ── DICTIONARIES — ORGANISING SENSOR DATA ────────────────

# A detected object in ADAS has many properties
# Dictionary stores them all together neatly
detected_vehicle = {
    "class_name": "Car",
    "confidence": 0.92,
    "bounding_box": [245, 180, 420, 310],  # [x1, y1, x2, y2] in pixels
    "distance": 15.3,                        # metres (from LiDAR)
    "velocity": 12.5,                        # m/s (from radar/EKF)
    "track_id": 7,                           # persistent ID across frames
    "time_to_collision": 1.22,              # seconds (for AEB decision)
}

# Access values
print("\n=== Detected Vehicle ===")
print(f"Class: {detected_vehicle['class_name']}")
print(f"Distance: {detected_vehicle['distance']}m")
print(f"TTC: {detected_vehicle['time_to_collision']}s")
print(f"Bounding box: {detected_vehicle['bounding_box']}")

# Update a value (as object moves closer)
detected_vehicle["distance"] = 14.1
detected_vehicle["time_to_collision"] = 1.13

# Add a new key
detected_vehicle["aeb_triggered"] = detected_vehicle["time_to_collision"] < 1.6

print(f"\nUpdated distance: {detected_vehicle['distance']}m")
print(f"AEB triggered: {detected_vehicle['aeb_triggered']}")

# ── SENSOR STATUS DICTIONARY ──────────────────────────────
sensor_status = {
    "CAMERA_FRONT": {"active": True,  "fps": 30, "resolution": "1280x720"},
    "LIDAR_TOP":    {"active": True,  "fps": 10, "points": 120000},
    "RADAR_FRONT":  {"active": True,  "fps": 20, "range": 200},
    "CAMERA_REAR":  {"active": False, "fps": 0,  "resolution": "1280x720"},
}

print("\n=== Sensor Health Check ===")
for sensor_name, info in sensor_status.items():
    status = "✅ ACTIVE" if info["active"] else "❌ OFFLINE"
    print(f"  {sensor_name:20s}: {status}")

# Count active sensors
active_count = sum(1 for s in sensor_status.values() if s["active"])
print(f"\nActive sensors: {active_count}/{len(sensor_status)}")

if active_count < 2:
    print("⚠️  WARNING: Too few sensors active. ADAS degraded mode.")



# ── FUNCTIONS — REUSABLE ADAS LOGIC ─────────────────────

def calculate_ttc(distance_m, closing_speed_ms):
    """
    Calculate Time to Collision (TTC).

    This is one of the most important functions in AEB systems.
    TTC = distance / closing_speed

    Args:
        distance_m: distance to object in metres
        closing_speed_ms: closing speed in metres per second
                          (positive = approaching, negative = moving away)

    Returns:
        TTC in seconds, or float('inf') if not approaching
    """
    if closing_speed_ms <= 0:
        return float('inf')   # not approaching — no collision risk
    return distance_m / closing_speed_ms


def aeb_decision(ttc_seconds):
    """
    Make AEB (Automatic Emergency Braking) decision based on TTC.

    This mirrors the real Bosch AEB decision cascade:
    - TTC > 3.5s: no action
    - TTC < 3.5s: pre-alert (prepare brakes)
    - TTC < 2.5s: visual warning to driver
    - TTC < 1.6s: partial braking (30%)
    - TTC < 0.8s: full emergency braking (100%)

    Args:
        ttc_seconds: time to collision in seconds

    Returns:
        tuple: (action_name, brake_percentage)
    """
    if ttc_seconds > 3.5:
        return ("NO_ACTION", 0)
    elif ttc_seconds > 2.5:
        return ("PRE_ALERT", 0)
    elif ttc_seconds > 1.6:
        return ("WARNING", 0)
    elif ttc_seconds > 0.8:
        return ("PARTIAL_BRAKE", 30)
    else:
        return ("FULL_BRAKE", 100)


def is_in_danger_zone(distance_m, object_class):
    """
    Check if object is in the danger zone requiring attention.

    Different object types have different danger distances:
    - Pedestrian: danger within 15m (they can change direction suddenly)
    - Cyclist: danger within 12m
    - Car: danger within 20m
    - Truck: danger within 25m (longer braking distance needed)

    Args:
        distance_m: distance to object in metres
        object_class: string class name

    Returns:
        True if object is in danger zone
    """
    danger_distances = {
        "Pedestrian": 15.0,
        "Cyclist": 12.0,
        "Car": 20.0,
        "Truck": 25.0,
        "Motorcycle": 12.0,
    }
    threshold = danger_distances.get(object_class, 20.0)
    return distance_m < threshold


# ── TEST YOUR FUNCTIONS ──────────────────────────────────
print("\n=== AEB System Simulation ===")

# Simulate 5 scenarios
scenarios = [
    {"distance": 50.0, "speed": 5.0,  "class": "Car"},
    {"distance": 30.0, "speed": 12.0, "class": "Car"},
    {"distance": 15.0, "speed": 10.0, "class": "Pedestrian"},
    {"distance": 8.0,  "speed": 15.0, "class": "Car"},
    {"distance": 3.0,  "speed": 20.0, "class": "Truck"},
]

for i, scenario in enumerate(scenarios, 1):
    ttc = calculate_ttc(scenario["distance"], scenario["speed"])
    action, brake_pct = aeb_decision(ttc)
    danger = is_in_danger_zone(scenario["distance"], scenario["class"])

    print(f"\nScenario {i}: {scenario['class']} at "
          f"{scenario['distance']}m, speed {scenario['speed']}m/s")
    print(f"  TTC: {ttc:.2f}s")
    print(f"  AEB Action: {action} | Brake: {brake_pct}%")
    print(f"  Danger Zone: {'YES ⚠️' if danger else 'No'}")

    # ── CONTROL FLOW — ADAS DECISION MAKING ──────────────────

def process_adas_frame(frame_number, detections_list):
    """
    Process one frame of ADAS data.
    This is the simplified version of what runs 30 times per second
    in a real ADAS ECU.

    Args:
        frame_number: current frame index
        detections_list: list of dicts with object info
    """
    print(f"\n{'='*50}")
    print(f"FRAME {frame_number:04d} — Processing {len(detections_list)} detections")
    print(f"{'='*50}")

    # Sort detections by distance (closest first — highest priority)
    sorted_detections = sorted(detections_list,
                               key=lambda x: x["distance"])

    critical_alert = False
    for obj in sorted_detections:
        ttc = calculate_ttc(obj["distance"], obj.get("speed", 10.0))
        action, brake = aeb_decision(ttc)
        danger = is_in_danger_zone(obj["distance"], obj["class"])

        # Only print objects that need attention
        if danger or action != "NO_ACTION":
            print(f"  ⚠️  {obj['class']:12s} | "
                  f"Dist: {obj['distance']:5.1f}m | "
                  f"TTC: {ttc:.1f}s | "
                  f"Action: {action}")
            if brake > 0:
                critical_alert = True
                print(f"       🚨 BRAKING: {brake}%")

    if not critical_alert:
        print("  ✅ All clear — normal operation")

    return critical_alert


# Simulate 3 frames of ADAS processing
frame_data = [
    # Frame 0 — clear road
    [
        {"class": "Car", "distance": 45.0, "speed": 2.0},
        {"class": "Car", "distance": 60.0, "speed": 0.5},
    ],
    # Frame 1 — car getting closer
    [
        {"class": "Car", "distance": 22.0, "speed": 8.0},
        {"class": "Pedestrian", "distance": 11.0, "speed": 5.0},
    ],
    # Frame 2 — emergency
    [
        {"class": "Car", "distance": 6.0, "speed": 18.0},
        {"class": "Pedestrian", "distance": 3.0, "speed": 12.0},
    ],
]

for frame_num, detections in enumerate(frame_data):
    critical = process_adas_frame(frame_num, detections)