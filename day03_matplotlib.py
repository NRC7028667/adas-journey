# =======================
# DAY 3 — MATPLOTLIB 
# =======================

# This MUST be the first two lines before anything else
# It tells Matplotlib: save graphs as image files
# instead of trying to open a popup window
import matplotlib
matplotlib.use('Agg')

# pyplot is the part of Matplotlib that draws graphs
# We give it a short nickname 'plt' so we type less
import matplotlib.pyplot as plt

# We need NumPy for creating number arrays to plot
import numpy as np

print("Everything imported successfully.")
print("Graphs will be saved as PNG image files.")

# ── STEP 5: YOUR VERY FIRST GRAPH ──────────────────────────

# Step 1: Create a Figure
# figsize controls width and height in inches
# (8, 5) means 8 inches wide and 5 inches tall
# dpi=120 means 120 dots per inch — higher number = sharper image
fig = plt.figure(figsize=(8, 5), dpi=120)

# Step 2: Add Axes to the Figure
# add_subplot(1, 1, 1) means:
# 1 row of graphs, 1 column of graphs, use the 1st slot
ax = fig.add_subplot(1, 1, 1)

# Step 3: Give data to the Axes
# We need two lists: one for X values and one for Y values
# Each pair (x[i], y[i]) becomes one point on the graph
x = [1, 2, 3, 4, 5]       # time in seconds
y = [50, 40, 30, 20, 10]  # distance to car ahead in metres

# ax.plot() draws a line connecting all the points
ax.plot(x, y)

# Step 4: Add title and labels
ax.set_xlabel("Time (seconds)")
ax.set_ylabel("Distance (metres)")

# Step 5: Save the Figure as a PNG file
# bbox_inches='tight' removes extra white space around the edges
fig.savefig("graph01_first_graph.png", bbox_inches='tight', dpi=120)

# Step 6: Close the Figure (frees up memory)
plt.close(fig)

print("\nSaved: graph01_first_graph.png")

# ── STEP 6: MAKING THE GRAPH BETTER ────────────────────────

# Create some realistic data
# This simulates a car approaching from 50m and getting closer
time_seconds  = [0, 1, 2, 3, 4, 5, 6, 7]
distance_metres = [50, 46, 41, 35, 27, 18, 11, 6]

fig = plt.figure(figsize=(9, 5), dpi=120)
ax = fig.add_subplot(1, 1, 1)

# ── MAKING THE LINE LOOK NICE ────────────────────────────────

# color: what colour the line is
# linewidth: how thick the line is (default is 1)
# linestyle: '-' is solid, '--' is dashed, ':' is dotted
# marker: shape drawn at each data point
#         'o' = circle, 's' = square, '^' = triangle
# markersize: how big each marker is
# label: text shown in the legend (explains what this line is)
ax.plot(time_seconds,
        distance_metres,
        color='steelblue',
        linewidth=2.5,
        linestyle='-',
        marker='o',
        markersize=7,
        label='Distance to vehicle ahead')

# ── ADDING REFERENCE LINES ───────────────────────────────────

# axhline draws a horizontal line across the entire graph
# y=15 means the line sits at y=15 on the Y axis
# This represents our warning zone boundary
ax.axhline(y=15,
           color='orange',
           linewidth=2,
           linestyle='--',
           label='Warning zone (15m)')

# Another horizontal line for the emergency braking threshold
ax.axhline(y=8,
           color='red',
           linewidth=2,
           linestyle='--',
           label='Emergency brake zone (8m)')

# ── SHADING A DANGER REGION ──────────────────────────────────

# fill_between shades the area between two Y values
# This visually shows the danger region
ax.fill_between(time_seconds,  # X values
                0,              # lower Y boundary
                15,             # upper Y boundary
                color='red',    # fill colour
                alpha=0.10,    # alpha: 0=invisible, 1=solid
                label='Danger region')
# alpha=0.10 makes it 90% transparent so you can still see the line

# ── ADDING GRID LINES ────────────────────────────────────────

# Grid lines make it easier to read exact values
ax.grid(True,
        linestyle='--',
        color='gray',
        alpha=0.4)

# ── ADDING TITLE AND LABELS ──────────────────────────────────

ax.set_title("Vehicle Distance Over Time — AEB Scenario",
             fontsize=13,
             fontweight='bold')   # makes title text bold

ax.set_xlabel("Time (seconds)", fontsize=11)
ax.set_ylabel("Distance (metres)", fontsize=11)

# ── ADDING A LEGEND ──────────────────────────────────────────

# Legend shows what each line/colour means
# loc='upper right' puts it in the top right corner
ax.legend(loc='upper right', fontsize=9)

# ── SETTING AXIS LIMITS ──────────────────────────────────────

# set_xlim and set_ylim control what range is visible
ax.set_xlim(0, 7)
ax.set_ylim(0, 55)

# Save and close
fig.savefig("graph02_better_graph.png",bbox_inches='tight', dpi=120)
plt.close(fig)
print("\nSaved: graph02_better_graph.png")

# ── STEP 7: THE SHORTCUT ─────────────────────────────────────

# plt.subplots() creates a Figure AND one Axes at the same time
# fig is the Figure, ax is the Axes
# You use this shortcut for almost every graph from now on
fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

# Everything else stays the same
ax.plot([1, 2, 3], [10, 20, 15], color='steelblue', linewidth=2)
ax.set_title("Using the Shortcut")
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
ax.grid(True, linestyle='--', alpha=0.4)

fig.savefig("graph03_shortcut.png", bbox_inches='tight', dpi=120)
plt.close(fig)
print("\nSaved: graph03_shortcut.png")

# ── STEP 8: SCATTER PLOT ────────────────────────────────────

# Imagine you ran your YOLO model on 60 images
# For each detection you recorded:
# - how far away the object was (distance)
# - how confident the model was (confidence score)
# You want to know: does the model get less confident
# as objects get farther away?

np.random.seed(42)   # seed makes random numbers reproducible

# Generate 60 fake detections
# Objects range from 5m to 60m away
distances   = np.random.uniform(5, 60, 60)

# Confidence tends to decrease with distance
# (farther objects are smaller and harder to detect)
# We simulate this with a formula + some random noise
confidence  = 0.95 - (distances / 60) * 0.35
confidence  = confidence + np.random.randn(60) * 0.05
confidence  = np.clip(confidence, 0.3, 1.0)
# np.clip keeps all values between 0.3 and 1.0

fig, ax = plt.subplots(figsize=(8, 5), dpi=120)

# ax.scatter() draws dots instead of a line
# x and y are the values for each axis
# s=60 is the size of each dot (in points squared)
# alpha=0.7 makes dots slightly transparent
# edgecolors='white' adds a thin white border around each dot
ax.scatter(distances,
           confidence,
           color='steelblue',
           s=60,
           alpha=0.7,
           edgecolors='white',
           linewidths=0.5,
           label='Detections (n=60)')

# Add a horizontal line at the minimum confidence threshold
ax.axhline(y=0.60,
           color='red',
           linewidth=2,
           linestyle='--',
           label='Min threshold (0.60)')

# Count how many detections are below the threshold
below_threshold = np.sum(confidence < 0.60)
print(f"\nDetections below threshold: {below_threshold} out of 60")

# Add a text annotation directly on the graph
# This is a label you place at a specific (x, y) position
ax.text(x=35,          # x position of the text
        y=0.40,        # y position of the text
        s=f'{below_threshold} detections\nbelow threshold\n(filtered out)',
        fontsize=9,
        color='red',
        ha='center',   # horizontal alignment: 'center', 'left', 'right'
        va='center',   # vertical alignment
        bbox=dict(     # bbox adds a box around the text
            boxstyle='round',
            facecolor='white',
            edgecolor='red',
            alpha=0.8))

ax.set_title("YOLO Detection Confidence vs Object Distance",
             fontsize=12, fontweight='bold')
ax.set_xlabel("Distance to Object (metres)", fontsize=11)
ax.set_ylabel("Detection Confidence Score", fontsize=11)
ax.set_xlim(0, 65)
ax.set_ylim(0.25, 1.05)
ax.legend(fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)

fig.savefig("graph04_scatter.png", bbox_inches='tight', dpi=120)
plt.close(fig)
print("Saved: graph04_scatter.png")

# ── STEP 9: HISTOGRAM ────────────────────────────────────────

# Imagine your radar sensor takes 200 measurements of the
# same object that is exactly 25.0 metres away
# Due to noise the readings are never exactly 25.0
# They are slightly different each time
# A histogram shows you how the errors are distributed

np.random.seed(10)

true_distance = 25.0

# np.random.randn gives numbers from a bell curve (normal distribution)
# Multiplying by 0.8 means most readings are within 0.8m of true value
measurement_errors = np.random.randn(200) * 0.8

# The actual readings are the true value plus the error
sensor_readings = true_distance + measurement_errors

fig, ax = plt.subplots(figsize=(9, 5), dpi=120)

# ax.hist() draws a histogram
# bins=25 means divide the range of values into 25 groups
# and draw one bar for each group
# the height of each bar shows how many readings fell in that range
ax.hist(sensor_readings,
        bins=25,
        color='steelblue',
        edgecolor='white',
        linewidth=0.5,
        alpha=0.85)

# Add a vertical line at the TRUE distance (25.0m)
ax.axvline(x=true_distance,
           color='green',
           linewidth=2.5,
           linestyle='-',
           label=f'True distance ({true_distance}m)')

# Add vertical lines at mean of the readings
mean_reading = sensor_readings.mean()
ax.axvline(x=mean_reading,
           color='orange',
           linewidth=2,
           linestyle='--',
           label=f'Mean reading ({mean_reading:.2f}m)')

# Add lines showing one standard deviation either side
std = sensor_readings.std()
ax.axvline(x=true_distance + std,
           color='red',
           linewidth=1.5,
           linestyle=':',
           label=f'+1 std dev ({std:.2f}m)')
ax.axvline(x=true_distance - std,
           color='red',
           linewidth=1.5,
           linestyle=':',
           label=f'-1 std dev ({std:.2f}m)')

ax.set_title("Radar Sensor Noise Distribution\n"
             "200 readings of an object at exactly 25.0 metres",
             fontsize=12, fontweight='bold')
ax.set_xlabel("Sensor Reading (metres)", fontsize=11)
ax.set_ylabel("Number of Readings (count)", fontsize=11)
ax.legend(fontsize=9)
ax.grid(True, axis='y', linestyle='--', alpha=0.6)

# Print the statistics in the terminal too
print(f"\nRadar Sensor Statistics:")
print(f"  True distance : {true_distance:.1f} m")
print(f"  Mean reading  : {mean_reading:.3f} m")
print(f"  Std deviation : {std:.3f} m")
print(f"  Min reading   : {sensor_readings.min():.3f} m")
print(f"  Max reading   : {sensor_readings.max():.3f} m")
print(f"  Error (mean vs true): {abs(mean_reading - true_distance):.4f} m")

fig.savefig("graph05_histogram.png", bbox_inches='tight', dpi=120)
plt.close(fig)
print("Saved: graph05_histogram.png\n")

# ── STEP 10: BAR CHART ───────────────────────────────────────

from matplotlib.patches import Patch

classes   = ['Car', 'Van', 'Truck', 'Pedestrian', 'Cyclist', 'Tram']
ap_scores = [0.89,  0.74,  0.71,   0.68,          0.72,      0.63]

fig, ax = plt.subplots(figsize=(9, 5), dpi=120)

bar_colours = []
for score in ap_scores:
    if score >= 0.80:
        bar_colours.append('mediumseagreen')
    elif score >= 0.70:
        bar_colours.append('goldenrod')
    else:
        bar_colours.append('tomato')

bars = ax.bar(classes,
              ap_scores,
              color=bar_colours,
              edgecolor='white',
              linewidth=0.8,
              width=0.55)

for bar, score in zip(bars, ap_scores):
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f'{score:.2f}',
            ha='center',
            va='bottom',
            fontsize=10,
            fontweight='bold')

ax.axhline(y=0.80,
           color='green',
           linewidth=2,
           linestyle='--',
           alpha=0.7)

ax.text(5.45,
        0.805,
        'Target (0.80)',
        fontsize=8,
        color='green',
        va='bottom',
        ha='right')

ax.set_title("YOLOv8 Detection Performance Per Class — KITTI Dataset",
             fontsize=12,
             fontweight='bold',
             pad=15)
ax.set_xlabel("Object Class", fontsize=11)
ax.set_ylabel("Average Precision (AP)", fontsize=11)
ax.set_ylim(0, 1.05)
ax.grid(True, axis='y', linestyle='--', alpha=0.4)

legend_items = [
    Patch(facecolor='mediumseagreen', label='Good  (>= 0.80)'),
    Patch(facecolor='goldenrod',      label='Acceptable  (>= 0.70)'),
    Patch(facecolor='tomato',         label='Needs work  (< 0.70)'),
]
ax.legend(handles=legend_items, fontsize=9, loc='upper right')

fig.savefig("graph06_bar_chart.png", bbox_inches='tight', dpi=120)
plt.close(fig)
print("Saved: graph06_bar_chart.png\n\n")

# ── STEP 11: MULTIPLE GRAPHS — SUBPLOTS ─────────────────────

# This creates one image with 4 graphs arranged in a 2x2 grid
# Top left, top right, bottom left, bottom right
# This kind of combined image is what goes in your GitHub README

np.random.seed(5)

# Create some data for each of the 4 graphs
frames      = np.arange(0, 100)              # 100 frames
distances   = 50 - frames * 0.4 + np.random.randn(100) * 1.5
confidence  = 0.80 + np.random.randn(100) * 0.07
confidence  = np.clip(confidence, 0.4, 1.0)
ttc_values  = distances / 8.0
ttc_values  = np.clip(ttc_values, 0, 12)
obj_counts  = np.random.poisson(4, 100)

# ── CREATE THE 2x2 GRID ──────────────────────────────────────

# plt.subplots(rows, cols) creates a grid of graphs
# nrows=2, ncols=2 means 2 rows and 2 columns = 4 graphs
# figsize is the TOTAL size of the whole image
fig, axes = plt.subplots(nrows=2, ncols=2,
                          figsize=(12, 8), dpi=120)

# axes is now a 2D grid you access like this:
# axes[0][0] = top left
# axes[0][1] = top right
# axes[1][0] = bottom left
# axes[1][1] = bottom right

# ── TOP LEFT GRAPH: Distance over time ──────────────────────
axes[0][0].plot(frames, distances,
                color='steelblue', linewidth=1.5)
axes[0][0].axhline(y=15, color='red', linewidth=1.5,
                   linestyle='--', label='Danger zone')
axes[0][0].fill_between(frames, 0, 15,
                         color='red', alpha=0.08)
axes[0][0].set_title("Distance to Nearest Vehicle",
                      fontsize=10, fontweight='bold')
axes[0][0].set_xlabel("Frame", fontsize=9)
axes[0][0].set_ylabel("Distance (m)", fontsize=9)
axes[0][0].legend(fontsize=8)
axes[0][0].grid(True, linestyle='--', alpha=0.3)
axes[0][0].set_ylim(0, 55)

# ── TOP RIGHT GRAPH: Confidence over time ───────────────────
axes[0][1].plot(frames, confidence,
                color='mediumseagreen', linewidth=1.5)
axes[0][1].axhline(y=0.60, color='red', linewidth=1.5,
                   linestyle='--', label='Min threshold')
axes[0][1].set_title("Detection Confidence Over Time",
                      fontsize=10, fontweight='bold')
axes[0][1].set_xlabel("Frame", fontsize=9)
axes[0][1].set_ylabel("Confidence Score", fontsize=9)
axes[0][1].legend(fontsize=8)
axes[0][1].grid(True, linestyle='--', alpha=0.3)
axes[0][1].set_ylim(0.3, 1.05)

# ── BOTTOM LEFT GRAPH: TTC over time ────────────────────────
axes[1][0].plot(frames, ttc_values,
                color='mediumpurple', linewidth=1.5)
axes[1][0].axhspan(0, 1.6, color='red', alpha=0.15,
                   label='Emergency (<1.6s)')
axes[1][0].axhspan(1.6, 2.5, color='orange', alpha=0.10,
                   label='Warning (1.6-2.5s)')
axes[1][0].set_title("Time to Collision (TTC)",
                      fontsize=10, fontweight='bold')
axes[1][0].set_xlabel("Frame", fontsize=9)
axes[1][0].set_ylabel("TTC (seconds)", fontsize=9)
axes[1][0].legend(fontsize=7)
axes[1][0].grid(True, linestyle='--', alpha=0.3)
axes[1][0].set_ylim(0, 12)

# ── BOTTOM RIGHT GRAPH: Object count histogram ──────────────
axes[1][1].hist(obj_counts, bins=10,
                color='darkorange',
                edgecolor='white',
                linewidth=0.5)
axes[1][1].axvline(x=obj_counts.mean(),
                   color='black', linewidth=2,
                   linestyle='-',
                   label=f'Mean: {obj_counts.mean():.1f}')
axes[1][1].set_title("Objects Detected Per Frame",
                      fontsize=10, fontweight='bold')
axes[1][1].set_xlabel("Number of Objects", fontsize=9)
axes[1][1].set_ylabel("Frame Count", fontsize=9)
axes[1][1].legend(fontsize=8)
axes[1][1].grid(True, axis='y', linestyle='--', alpha=0.3)

# ── MAIN TITLE FOR THE WHOLE IMAGE ──────────────────────────
fig.suptitle("ADAS System Performance Dashboard — 100 Frames",
             fontsize=14,
             fontweight='bold')

# tight_layout automatically adjusts spacing so graphs
# do not overlap each other
fig.tight_layout(pad=2.5)

fig.savefig("graph07_dashboard.png", bbox_inches='tight', dpi=120)
plt.close(fig)
print("Saved: graph07_dashboard.png")