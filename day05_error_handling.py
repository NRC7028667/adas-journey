# ============================================================
# DAY 5 — ERROR HANDLING FROM ABSOLUTE ZERO
# ============================================================

# ── CONCEPT 1: WHAT HAPPENS WITHOUT ERROR HANDLING ──────────
''' remove this to see the error(''' ''')
print("Program started")

# This will crash because you cannot divide by zero
result = 10 / 0

print("This line never runs")'''

# ── CONCEPT 2: TRY AND EXCEPT ────────────────────────────────

# The structure is:
#
# try:
#     code that might fail
# except:
#     what to do if it fails

print("\n--- Example 1: Basic try except ---")

try:
    result = 10 / 0
    print("This will not run")
except:
    print("Something went wrong — but program did not crash")

print("Program continues after the error")
# ── CONCEPT 3: SPECIFIC ERROR TYPES ─────────────────────────

# ZeroDivisionError — dividing by zero
print("\n--- ZeroDivisionError ---")
try:
    answer = 100 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")


# TypeError — wrong type of data
print("\n--- TypeError ---")
try:
    result = "hello" + 5
    # Cannot add text and number together
except TypeError:
    print("Cannot add text and number together")


# NameError — using a variable that does not exist
print("\n--- NameError ---")
try:
    print(undefined_variable)
except NameError:
    print("That variable does not exist")


# IndexError — going outside list boundaries
print("\n--- IndexError ---")
try:
    my_list = [1, 2, 3]
    print(my_list[10])    # list only has index 0, 1, 2
except IndexError:
    print("That index does not exist in the list")


# ValueError — right type but wrong value
print("\n--- ValueError ---")
try:
    number = int("hello")   # cannot convert "hello" to integer
except ValueError:
    print("Cannot convert that text to a number")

# ── CONCEPT 4: READING THE ERROR MESSAGE ─────────────────────

print("\n--- Reading the error message ---")

try:
    result = 50 / 0

# 'as e' gives you the error object stored in variable e
# str(e) converts it to text so you can print it
except ZeroDivisionError as e:
    print(f"Error occurred: {e}")
    print(f"Error type: {type(e).__name__}")


# Another example
print()
try:
    number = int("not_a_number")
except ValueError as e:
    print(f"Error occurred: {e}")
    print(f"Error type: {type(e).__name__}")

    # ── CONCEPT 5: ELSE AND FINALLY ─────────────────────────────

print("\n--- else and finally ---")

# Example with no error
print("Test 1: No error")
try:
    result = 100 / 4
except ZeroDivisionError:
    print("Division failed")
else:
    # This runs ONLY if try succeeded with no error
    print(f"Division succeeded: {result}")
finally:
    # This ALWAYS runs no matter what
    print("This always runs")


print()

# Example with error
print("Test 2: With error")
try:
    result = 100 / 0
except ZeroDivisionError:
    print("Division failed")
else:
    # This does NOT run because there was an error
    print(f"Division succeeded: {result}")
finally:
    # This ALWAYS runs no matter what
    print("This always runs")

# ── CONCEPT 6: MULTIPLE EXCEPT BLOCKS ───────────────────────

def process_sensor_reading(reading, index, sensor_list):
    """
    Try to process a sensor reading safely.
    Different things can go wrong so we handle each separately.
    """
    print(f"\nProcessing reading: {reading}, index: {index}")

    try:
        # Three things that could go wrong here:
        # 1. index might be outside list
        # 2. reading might not be a number
        # 3. some calculation might fail

        sensor_name = sensor_list[index]   # could be IndexError
        value       = float(reading)       # could be ValueError
        result      = 100 / value          # could be ZeroDivisionError

        print(f"Sensor: {sensor_name}")
        print(f"Value : {value}")
        print(f"Result: {result:.2f}")
        return result

    except IndexError:
        print(f"No sensor at index {index}")
        return None

    except ValueError:
        print(f"Reading '{reading}' is not a valid number")
        return None

    except ZeroDivisionError:
        print("Reading is zero — cannot process")
        return None


# Test with different situations
sensors = ["CAMERA", "RADAR", "LIDAR"]

process_sensor_reading("25.5", 0, sensors)   # works fine
process_sensor_reading("abc",  1, sensors)   # bad value
process_sensor_reading("25.5", 9, sensors)   # bad index
process_sensor_reading("0",    2, sensors)   # zero value

# ── CONCEPT 7: RAISING YOUR OWN ERRORS ──────────────────────

def set_sensor_range(range_metres):
    """
    Set the detection range for a sensor.
    Range must be between 1 and 300 metres.
    If not — we raise an error ourselves.
    """

    # Check if value makes sense for a sensor
    if range_metres < 1:
        raise ValueError(f"Range {range_metres}m is too small. Minimum is 1m")

    if range_metres > 300:
        raise ValueError(f"Range {range_metres}m is too large. Maximum is 300m")

    if not isinstance(range_metres, (int, float)):
        raise TypeError("Range must be a number")

    print(f"Sensor range set to {range_metres} metres")
    return range_metres


# Test with valid value
print("\n\n--- Valid range ---")
try:
    set_sensor_range(150)
except ValueError as e:
    print(f"Error: {e}")

# Test with too small
print("\n--- Too small ---")
try:
    set_sensor_range(-5)
except ValueError as e:
    print(f"Error: {e}")

# Test with too large
print("\n--- Too large ---")
try:
    set_sensor_range(500)
except ValueError as e:
    print(f"Error: {e}")

# ── CONCEPT 8: COMPLETE ADAS SENSOR READER ──────────────────

class SafeSensorReader:
    """
    Reads sensor data safely.
    Never crashes even if sensor gives bad data.
    """

    def __init__(self, sensor_name):
        self.sensor_name  = sensor_name
        self.good_readings = []
        self.error_count   = 0

    def read(self, raw_value):
        """
        Try to read one value from sensor.
        Handle all possible failures.
        """
        try:
            # Convert raw value to float
            value = float(raw_value)

            # Check value makes physical sense
            # Distance readings should be between 0 and 300 metres
            if value < 0:
                raise ValueError(f"Negative distance: {value}")
            if value > 300:
                raise ValueError(f"Distance too large: {value}")

            # If we get here everything is fine
            self.good_readings.append(value)
            print(f"{self.sensor_name}: {value:.2f}m  OK")
            return value

        except ValueError as e:
            self.error_count += 1
            print(f"{self.sensor_name}: BAD READING — {e}")
            return None

        except Exception as e:
            # Catch anything else unexpected
            self.error_count += 1
            print(f"{self.sensor_name}: UNKNOWN ERROR — {e}")
            return None

    def get_summary(self):
        print(f"\n--- {self.sensor_name} Summary ---")
        print(f"Good readings : {len(self.good_readings)}")
        print(f"Errors        : {self.error_count}")
        if self.good_readings:
            avg = sum(self.good_readings) / len(self.good_readings)
            print(f"Average       : {avg:.2f}m")
            print(f"Min distance  : {min(self.good_readings):.2f}m")
            print(f"Max distance  : {max(self.good_readings):.2f}m")


# Create a sensor reader and feed it mixed data
radar = SafeSensorReader("RADAR_FRONT")

print("=== Reading Radar Data ===\n")

# Mix of good and bad readings
radar.read(45.2)       # good
radar.read(38.7)       # good
radar.read("abc")      # bad — not a number
radar.read(22.1)       # good
radar.read(-5.0)       # bad — negative
radar.read(15.8)       # good
radar.read(999)        # bad — too large
radar.read(8.3)        # good

# Show summary
radar.get_summary()