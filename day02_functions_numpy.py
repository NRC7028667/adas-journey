# ============================================================
# DAY 2 — FUNCTIONS AND NUMPY FROM SCRATCH
# ============================================================

# ── PART 1: UNDERSTANDING EVERY PART OF A FUNCTION ─────────

# The word 'def' tells Python "I am creating a function"
# 'greet_engineer' is the name of the function
# The parentheses () is where inputs go
# The colon : starts the function body
def greet_engineer():
    # Everything indented inside belongs to this function
    # Indentation means 4 spaces or 1 Tab
    print("Hello ADAS Engineer!")
    print("Welcome to Day 2.")

# The function is defined above but has NOT run yet
# To run it you must CALL it by writing its name with ()
greet_engineer()
greet_engineer()
greet_engineer()

# A function that takes inputs is more useful
# 'name' and 'role' are called PARAMETERS
# They are like empty boxes that get filled when you call the function
def introduce_engineer(name, role):
    print(f"\n\nName: {name}")
    print(f"Role: {role}")
    print(f"{name} is training to become an {role}")
    print("---")

# When you CALL the function you give it ARGUMENTS
# Arguments fill the parameter boxes
introduce_engineer("XYZ", "ADAS Engineer")
introduce_engineer("Ravi", "Computer Vision Engineer")
introduce_engineer("Priya", "Robotics Engineer")

# Some functions give you a result back
# The 'return' keyword sends a value back to whoever called the function

def add_numbers(a, b):
    result = a + b
    return result       # this sends the value back

# The returned value goes into the variable on the left
sum1 = add_numbers(5, 3)      # sum1 becomes 8
sum2 = add_numbers(100, 250)  # sum2 becomes 350

print(f"\n\n5 + 3 = {sum1}")
print(f"100 + 250 = {sum2}")

# You can use the return value directly without storing it
print(f"10 + 20 = {add_numbers(10, 20)}")

# Sometimes you want a parameter to have a default value
# if the caller does not provide it

# 'unit' has a default value of "metres"
# If you call the function without specifying unit, it uses "metres"
def print_distance(distance, unit="metres"):
    print(f"\n\nDistance: {distance} {unit}")

print_distance(25.5)              # uses default unit "metres"
print_distance(255.5, "metres")    # same result, explicit
print_distance(83.7, "feet")      # overrides default with "feet"

# A docstring is a description of what the function does
# It goes right after the def line inside triple quotes
# This is what Bosch engineers read to understand your code

def calculate_ttc(distance_m, closing_speed_ms):
    """
    Calculate Time To Collision (TTC).

    TTC is one of the most critical calculations in AEB systems.
    It tells the car how many seconds until it hits the object ahead.

    Formula: TTC = distance / closing_speed

    Parameters:
        distance_m (float): distance to the object in metres
                            must be positive (greater than zero)
        closing_speed_ms (float): how fast you are approaching
                                  in metres per second
                                  positive = getting closer
                                  negative = getting farther away
                                  zero = same speed, not approaching

    Returns:
        float: time in seconds until collision
               returns infinity if not approaching (no risk)

    Examples:
        >>> calculate_ttc(30.0, 10.0)
        3.0
        >>> calculate_ttc(15.0, 0.0)
        inf
    """
    # Guard clause: if not approaching, no collision risk
    if closing_speed_ms <= 0:
        return float('inf')

    # Main calculation
    ttc = distance_m / closing_speed_ms
    return ttc

# Test your function
print("\n\n=== TTC Calculations ===")
print(f"30m at 10m/s  → TTC = {calculate_ttc(30.0, 10.0):.1f}s")
print(f"15m at 10m/s  → TTC = {calculate_ttc(15.0, 10.0):.1f}s")
print(f"15m at 0m/s   → TTC = {calculate_ttc(15.0, 0.0)}")
print(f"15m at -5m/s  → TTC = {calculate_ttc(15.0, -5.0)}")

# Python functions can return more than one value
# This is very useful in ADAS where you often need multiple results

def analyse_detection(distance_m, confidence, object_class):
    """
    Analyse a single detection and return multiple pieces of information.

    Returns:
        tuple: (is_dangerous, priority_level, recommended_action)
    """
    # Is this object dangerous?
    is_dangerous = distance_m < 20.0 and confidence > 0.7

    # Priority level: 1=low, 2=medium, 3=high, 4=critical
    if distance_m > 50:
        priority = 1
    elif distance_m > 30:
        priority = 2
    elif distance_m > 15:
        priority = 3
    else:
        priority = 4

    # What should the system do?
    if priority == 4 and is_dangerous:
        action = "EMERGENCY_BRAKE"
    elif priority == 3:
        action = "WARNING_ALERT"
    elif priority == 2:
        action = "MONITOR_CLOSELY"
    else:
        action = "NORMAL_OPERATION"

    return is_dangerous, priority, action

# Unpack the three returned values into three variables
dangerous, priority, action = analyse_detection(
    distance_m=12.0,
    confidence=0.89,
    object_class="Pedestrian"
)

print(f"\n\nDangerous: {dangerous}")
print(f"Priority: {priority}")
print(f"Action: {action}")

# Test multiple scenarios
print("\n=== Detection Analysis Results ===")
scenarios = [
    (60.0, 0.91, "Car"),
    (35.0, 0.78, "Car"),
    (18.0, 0.85, "Pedestrian"),
    (8.0,  0.93, "Child"),
]

for dist, conf, cls in scenarios:
    danger, pri, act = analyse_detection(dist, conf, cls)
    print(f"{cls:12s} at {dist:5.1f}m → "
          f"Priority:{pri} | Action:{act}")
    

# ── PART 2: NUMPY FROM SCRATCH ──────────────────────────────

# Every NumPy file starts with this import
# 'as np' means we give it a shorter nickname 'np'
# So instead of typing 'numpy.array()' every time
# we just type 'np.array()'
import numpy as np

print("\n" + "="*50)
print("NUMPY FUNDAMENTALS")
print("="*50)

# ── UNDERSTANDING NUMPY ARRAYS ───────────────────────────────

# A regular Python list stores numbers like this:
python_list = [10, 20, 30, 40, 50]

# A NumPy array stores numbers like this:
numpy_array = np.array([10, 20, 30, 40, 50])

# They look similar but they are VERY different inside
# NumPy array: all numbers stored in continuous memory
#              can do math on all numbers at once
#              much faster for large data

print("Python list:", python_list)
print("NumPy array:", numpy_array)
print("Type of list:", type(python_list))
print("Type of array:", type(numpy_array))
print("NumPy dtype:", numpy_array.dtype)

# ── CREATING NUMPY ARRAYS ────────────────────────────────────

# Method 1: from a Python list
distances = np.array([15.3, 28.7, 8.2, 12.1, 45.6])
print("\nDistances array:", distances)

# Method 2: array of all zeros
# Used to initialise empty sensor buffers
empty_buffer = np.zeros(10)
print("Zeros:", empty_buffer)

# Method 3: array of all ones
ones_array = np.ones(5)
print("Ones:", ones_array)

# Method 4: evenly spaced numbers from start to stop
# Used for creating time axes, ranges, test data
time_axis = np.arange(0, 1.0, 0.1)  # from 0 to 1.0, step 0.1
print("Time axis:", time_axis)

# Method 5: N evenly spaced numbers between start and stop
# Different from arange: you specify HOW MANY points, not the step
frequencies = np.linspace(76e9, 77e9, 10)  # radar frequency sweep
print("Frequencies:", frequencies)

# Method 6: random numbers (for generating test data)
np.random.seed(42)   # seed makes random reproducible (same result every run)
noise = np.random.randn(5)  # 5 numbers from standard normal distribution
print("Random noise:", noise)

# Method 7: random integers
frame_ids = np.random.randint(0, 1000, size=5)
print("Random frame IDs:", frame_ids)

# ── UNDERSTANDING ARRAY SHAPE ────────────────────────────────

# Shape tells you the dimensions of an array
# This is CRITICAL for ADAS because:
# A camera image is a 3D array: (height, width, channels)
# A LiDAR scan is a 2D array: (num_points, 4) for x,y,z,intensity
# A batch of images is 4D: (batch_size, height, width, channels)

# 1D array — like a list of numbers
sensor_readings = np.array([1.2, 3.4, 5.6, 7.8, 9.0])
print("\n=== Understanding Shape ===")
print(f"1D array: {sensor_readings}")
print(f"Shape: {sensor_readings.shape}")    # (5,) means 5 elements
print(f"Dimensions: {sensor_readings.ndim}D") # 1 dimension
print(f"Total elements: {sensor_readings.size}") # 5 elements

# 2D array — like a table or a matrix
# Think of this as a spreadsheet with rows and columns
# In ADAS: a LiDAR point cloud where each row is one point
# and columns are x, y, z, intensity
lidar_points = np.array([
    [1.5,  2.3,  0.1,  45.0],   # point 1: x=1.5, y=2.3, z=0.1, intensity=45
    [3.2,  1.1, -0.2,  67.0],   # point 2
    [5.7,  4.8,  0.3,  23.0],   # point 3
    [2.1,  6.2, -0.1,  89.0],   # point 4
    [8.3,  3.5,  0.2,  34.0],   # point 5
])
print(f"\n2D array (LiDAR points):")
print(lidar_points)
print(f"Shape: {lidar_points.shape}")  # (5, 4) means 5 rows, 4 columns
print(f"Dimensions: {lidar_points.ndim}D") # 2 dimensions

# 3D array — like a colour image
# In ADAS: every camera frame is a 3D NumPy array
# Shape: (height, width, channels) where channels=3 for RGB
fake_image = np.zeros((480, 640, 3), dtype=np.uint8)
print(f"\n3D array (camera image):")
print(f"Shape: {fake_image.shape}")
print(f"Height: {fake_image.shape[0]} pixels")
print(f"Width: {fake_image.shape[1]} pixels")
print(f"Channels: {fake_image.shape[2]} (R, G, B)")
print(f"Total pixels: {fake_image.shape[0] * fake_image.shape[1]}")

# ── INDEXING AND SLICING ─────────────────────────────────────

# Think of indexing like addressing: row 2, column 3
# In Python counting starts at 0, not 1

distances = np.array([15.3, 28.7, 8.2, 12.1, 45.6, 33.2, 7.8])

print("\n=== Indexing and Slicing ===")
print(f"Full array: {distances}")
print(f"First element (index 0): {distances[0]}")
print(f"Last element (index -1): {distances[-1]}")
print(f"Second element (index 1): {distances[1]}")
print(f"Third from last (index -3): {distances[-3]}")

# Slicing: get a range of elements
# syntax: array[start:stop]  (stop is NOT included)
print(f"\nFirst 3 elements [0:3]: {distances[0:3]}")
print(f"Elements 2 to 4 [2:5]: {distances[2:5]}")
print(f"From index 3 onwards [3:]: {distances[3:]}")
print(f"Up to index 3 [:3]: {distances[:3]}")
print(f"Every 2nd element [::2]: {distances[::2]}")
print(f"Reversed [::-1]: {distances[::-1]}")

# 2D array indexing
print("\n=== 2D Array Indexing (LiDAR Points) ===")
print(f"First point (row 0): {lidar_points[0]}")
print(f"Third point (row 2): {lidar_points[2]}")
print(f"X coordinate of first point: {lidar_points[0, 0]}")
print(f"Y coordinate of third point: {lidar_points[2, 1]}")
print(f"All X coordinates (column 0): {lidar_points[:, 0]}")
print(f"All Y coordinates (column 1): {lidar_points[:, 1]}")
print(f"All Z coordinates (column 2): {lidar_points[:, 2]}")
print(f"First 3 points: \n{lidar_points[:3]}")

# ── MATH OPERATIONS ON ARRAYS ────────────────────────────────

# The magic of NumPy: math applies to ALL elements at once
# This is called VECTORISED OPERATIONS
# No need for loops!

sensor_data = np.array([10.5, 20.3, 15.7, 8.9, 25.1])

print("\n=== Array Math ===")
print(f"Original: {sensor_data}")

# Add a number to every element
print(f"Add 5 to all: {sensor_data + 5}")

# Multiply every element
print(f"Multiply by 2: {sensor_data * 2}")

# Subtract
print(f"Subtract 10: {sensor_data - 10}")

# Divide
print(f"Divide by 100: {sensor_data / 100}")

# Power
print(f"Square all: {sensor_data ** 2}")

# Math between two arrays (element by element)
array_a = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
array_b = np.array([10.0, 20.0, 30.0, 40.0, 50.0])

print(f"\nArray A: {array_a}")
print(f"Array B: {array_b}")
print(f"A + B: {array_a + array_b}")
print(f"A * B: {array_a * array_b}")
print(f"A / B: {array_a / array_b}")

# ── STATISTICS ON ARRAYS ─────────────────────────────────────

# Imagine you recorded 10 distance readings from a radar sensor
# The readings are slightly noisy (sensors are never perfect)

np.random.seed(0)
true_distance = 25.0  # the actual distance is 25 metres
noise = np.random.randn(10) * 0.5  # small noise, standard dev = 0.5m
radar_readings = true_distance + noise

print("\n=== Radar Sensor Statistics ===")
print(f"True distance: {true_distance} metres")
print(f"Radar readings: {radar_readings.round(2)}")
print(f"Minimum reading: {radar_readings.min():.3f}m")
print(f"Maximum reading: {radar_readings.max():.3f}m")
print(f"Mean (average): {radar_readings.mean():.3f}m")
print(f"Standard deviation: {radar_readings.std():.3f}m")
print(f"Median: {np.median(radar_readings):.3f}m")
print(f"Sum of all readings: {radar_readings.sum():.3f}")

# The mean is our best estimate of the true distance
error = abs(radar_readings.mean() - true_distance)
print(f"\nError from true distance: {error:.3f}m")
print("The mean is a better estimate than any single reading!")

# Find which reading has maximum/minimum value
print(f"\nIndex of min reading: {radar_readings.argmin()}")
print(f"Index of max reading: {radar_readings.argmax()}")

# ── BOOLEAN MASKING ──────────────────────────────────────────

# This is one of the most useful NumPy features for ADAS
# It lets you filter data based on conditions
# WITHOUT writing a loop

all_distances = np.array([15.3, 28.7, 8.2, 12.1, 45.6,
                           33.2, 7.8, 52.1, 19.4, 6.3])

print("\n=== Boolean Masking ===")
print(f"All distances: {all_distances}")

# Create a boolean mask: True where condition is met
danger_mask = all_distances < 15.0
print(f"\nDanger mask (dist < 15m): {danger_mask}")
print(f"This shows True where distance is less than 15 metres")

# Use the mask to filter: only get dangerous distances
dangerous_distances = all_distances[danger_mask]
print(f"Dangerous distances: {dangerous_distances}")
print(f"Number of dangerous objects: {len(dangerous_distances)}")

# You can write it in one line
very_close = all_distances[all_distances < 10.0]
print(f"\nVery close objects (<10m): {very_close}")

# Multiple conditions
# Objects that are close AND within a reasonable range
moderate_risk = all_distances[(all_distances >= 10.0) & (all_distances < 25.0)]
print(f"Moderate risk (10-25m): {moderate_risk}")

# Count how many satisfy condition
num_dangerous = np.sum(all_distances < 15.0)
print(f"\nTotal dangerous objects: {num_dangerous}")

# Percentage of objects in danger zone
percentage = (num_dangerous / len(all_distances)) * 100
print(f"Percentage in danger zone: {percentage:.2f}%")


# ── RESHAPING ARRAYS ─────────────────────────────────────────

# Sometimes you need to change the shape of an array
# This is very common in deep learning (changing image dimensions)
# and in sensor data processing

# Start with a 1D array of 12 numbers
flat_data = np.arange(12)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
print("\n=== Reshaping ===")
print(f"Original (1D): {flat_data}")
print(f"Shape: {flat_data.shape}")

# Reshape to 2D: 3 rows, 4 columns
matrix_3x4 = flat_data.reshape(3, 4)
print(f"\nReshaped to (3,4):\n{matrix_3x4}")
print(f"Shape: {matrix_3x4.shape}")

# Reshape to 4 rows, 3 columns
matrix_4x3 = flat_data.reshape(4, 3)
print(f"\nReshaped to (4,3):\n{matrix_4x3}")

# Flatten back to 1D
flattened = matrix_3x4.flatten()
print(f"\nFlattened back: {flattened}")

# -1 means "figure out this dimension automatically"
auto_reshape = flat_data.reshape(2, -1)  # 2 rows, auto columns
print(f"\nReshape(2,-1):\n{auto_reshape}")
print(f"Shape: {auto_reshape.shape}")  # (2, 6) because 12/2 = 6

# ── PUTTING IT ALL TOGETHER ──────────────────────────────────

def process_sensor_frame(frame_id, sensor_readings):
    """
    Process one frame of sensor data from multiple sensors.

    In a real ADAS system this runs every 50 milliseconds.
    This simplified version shows the key operations.

    Parameters:
        frame_id (int): which frame number this is
        sensor_readings (np.ndarray): shape (N, 4)
                                      columns: distance, confidence,
                                               speed, sensor_type

    Returns:
        dict: processed results for this frame
    """
    print(f"\n{'='*55}")
    print(f" FRAME {frame_id:04d} — Processing {len(sensor_readings)} readings")
    print(f"{'='*55}")

    # Extract each column into its own named array
    distances   = sensor_readings[:, 0]  # first column
    confidences = sensor_readings[:, 1]  # second column
    speeds      = sensor_readings[:, 2]  # third column

    # Step 1: Filter out low confidence readings
    # Below 0.6 confidence = unreliable, ignore it
    reliable_mask = confidences >= 0.6
    reliable_distances = distances[reliable_mask]
    reliable_speeds    = speeds[reliable_mask]

    print(f"\n Total readings : {len(distances)}")
    print(f" Reliable (≥0.6): {reliable_mask.sum()}")
    print(f" Filtered out   : {(~reliable_mask).sum()}")

    if len(reliable_distances) == 0:
        print(" No reliable readings! Sensor fault.")
        return None

    # Step 2: Statistics on reliable distances
    print(f"\n Distance Stats (reliable only):")
    print(f"  Minimum : {reliable_distances.min():.2f} m")
    print(f"  Maximum : {reliable_distances.max():.2f} m")
    print(f"  Average : {reliable_distances.mean():.2f} m")
    print(f"  Standard Deviation : {reliable_distances.std():.2f} m")

    # Step 3: Find objects in danger zone (< 20m)
    danger_mask    = reliable_distances < 20.0
    danger_dists   = reliable_distances[danger_mask]
    danger_speeds  = reliable_speeds[danger_mask]

    print(f"\n Objects in danger zone (<20m): {danger_mask.sum()}")

    # Step 4: Calculate TTC for each dangerous object
    if len(danger_dists) > 0:
        print(f"\n Dangerous Objects — TTC Analysis:")
        print(f"  {'Distance':>10} {'Speed':>10} {'TTC':>10} {'Action':>20}")
        print(f"  {'-'*52}")

        for dist, spd in zip(danger_dists, danger_speeds):
            ttc = calculate_ttc(dist, spd)
            _, _, action = analyse_detection(dist, 0.9, "Car")

            if ttc == float('inf'):
                ttc_str = "∞ (safe)"
            else:
                ttc_str = f"{ttc:.2f}s"

            print(f"  {dist:>8.1f}m  {spd:>8.1f}m/s"
                  f"  {ttc_str:>8}  {action:>20}")

    # Step 5: Overall frame assessment
    min_ttc = float('inf')
    for dist, spd in zip(danger_dists, danger_speeds):
        ttc = calculate_ttc(dist, spd)
        if ttc < min_ttc:
            min_ttc = ttc

    if min_ttc < 1.6:
        frame_status = "🚨 EMERGENCY BRAKE"
    elif min_ttc < 2.5:
        frame_status = "⚠️  WARNING"
    elif min_ttc < 3.5:
        frame_status = "🔶 CAUTION"
    else:
        frame_status = "✅ ALL CLEAR"

    print(f"\n Frame Status: {frame_status}")
    if min_ttc != float('inf'):
        print(f" Minimum TTC : {min_ttc:.2f}s")

    return {
        "frame_id": frame_id,
        "status": frame_status,
        "min_ttc": min_ttc,
        "danger_count": len(danger_dists),
        "reliable_count": len(reliable_distances),
    }


# ── SIMULATE 3 FRAMES ────────────────────────────────────────

# Generate test data for 3 frames
# Each row: [distance_m, confidence, speed_ms, sensor_type]
np.random.seed(42)

# Frame 0: clear road, all far away
frame_0 = np.array([
    [45.2, 0.92, 5.0, 1],
    [62.1, 0.78, 3.0, 1],
    [38.7, 0.45, 8.0, 2],   # low confidence, will be filtered
    [55.0, 0.81, 2.0, 1],
])

# Frame 1: some vehicles approaching
frame_1 = np.array([
    [18.3, 0.89, 12.0, 1],  # car approaching at 12 m/s
    [35.0, 0.76, 5.0,  1],
    [12.5, 0.92, 8.0,  2],  # cyclist close
    [8.2,  0.35, 15.0, 1],  # low confidence, filtered
    [28.0, 0.67, 3.0,  1],
])

# Frame 2: emergency situation
frame_2 = np.array([
    [5.1,  0.95, 20.0, 1],  # emergency! very close, fast
    [12.3, 0.88, 15.0, 2],  # also dangerous
    [3.8,  0.91, 18.0, 1],  # critical!
    [45.0, 0.72, 4.0,  1],  # safe
])

frames = [frame_0, frame_1, frame_2]
results = []

for i, frame_data in enumerate(frames):
    result = process_sensor_frame(i, frame_data)
    if result:
        results.append(result)

# Summary across all frames
print(f"\n{'='*55}")
print(" MISSION SUMMARY — 3 FRAMES PROCESSED")
print(f"{'='*55}")
for r in results:
    print(f" Frame {r['frame_id']}: {r['status']} | "
          f"Danger objects: {r['danger_count']} | "
          f"Reliable readings: {r['reliable_count']}")