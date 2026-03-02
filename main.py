import os
import fastf1
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Added for statistical analysis

# 1. Setup Cache
cache_folder = 'cache_folder'
if not os.path.exists(cache_folder):
    os.makedirs(cache_folder)
fastf1.Cache.enable_cache(cache_folder)

# 2. Load Session
print("Loading session....")
session = fastf1.get_session(2024, 'Australia', 'R')
session.load(telemetry=True, weather=False, messages=False)

# 3. Get specific laps (Pick fastest for a clean comparison)
print("Picking fastest laps for comparison...")
ham_lap = session.laps.pick_drivers('HAM').pick_fastest()
rus_lap = session.laps.pick_drivers('RUS').pick_fastest()

# 4. Get telemetry
print("Extracting telemetry...")
telemetry1 = ham_lap.get_telemetry()
telemetry2 = rus_lap.get_telemetry()

# 5. Filter columns (Your Shopping List)
cols = ['Time', 'Distance', 'X', 'Y', 'Z', 'RPM', 'Speed', 'nGear', 'Throttle']
engine_data1 = telemetry1[cols]
engine_data2 = telemetry2[cols]

print(engine_data1.head())
print(engine_data2.head())

# 6. Create the Dashboard
# sharex=True ensures both graphs zoom together on the 'Distance' axis
fig, (ax1, ax2, ax3,ax4) = plt.subplots(nrows=4, ncols=1, figsize=(12, 10), sharex=True)

# TOP GRAPH: Speed Comparison
ax1.plot(engine_data1['Distance'], engine_data1['Speed'], color='#00A19B', label='Hamilton')
ax1.plot(engine_data2['Distance'], engine_data2['Speed'], color='#C0C0C0', label='Russell', linestyle='--')
ax1.set_ylabel('Speed (km/h)')
ax1.set_title('Mercedes Teammate Comparison: Australia 2024')
ax1.legend()
ax1.grid(True, alpha=0.3)

# BOTTOM GRAPH: RPM Comparison
ax2.plot(engine_data1['Distance'], engine_data1['RPM'], color='#00A19B', label='Hamilton')
ax2.plot(engine_data2['Distance'], engine_data2['RPM'], color='#C0C0C0', label='Russell', linestyle='--')
ax2.set_ylabel('Engine RPM')
ax2.set_xlabel('Distance on Lap (m)')
ax2.legend()
ax2.grid(True, alpha=0.3) #alpha = transperency

ax3.plot(engine_data1['Distance'], engine_data1['Throttle'], color='#00A19B', label='Hamilton')
ax3.plot(engine_data2['Distance'], engine_data2['Throttle'], color='#C0C0C0',label='Russell', linestyle='--' )
ax3.set_ylabel('Engine Throttle')
ax3.set_xlabel('Distance on Lap')
ax3.legend()
ax3.grid(True,alpha = 0.3) 

ax4.plot(engine_data1['X'],engine_data1['Y'], color='#00A19B', label='Hamilton')
ax4.plot(engine_data2['X'],engine_data2['Y'],color='#C0C0C0',label='Russell', linestyle='--')
ax4.set_xlabel("X Coordinate")
ax4.set_ylabel("Y coordinate")
ax4.legend()
ax4.grid(True, alpha=0.3)

# 7. Show and Save
plt.tight_layout()
plt.show(block=False)

print(f"Data Loaded: Hamilton ({len(engine_data1)} rows), Russell ({len(engine_data2)} rows)")


# ─────────────────────────────────────────────────────────────
# 8. NUMPY ANALYSIS 
# ─────────────────────────────────────────────────────────────

# Converting speed and RPM columns into numpy arrays
ham_speed = np.array(engine_data1['Speed'])
rus_speed = np.array(engine_data2['Speed'])
ham_rpm = np.array(engine_data1['RPM'])
rus_rpm = np.array(engine_data2['RPM'])

# Basic stats for speed
print("\n--- Speed Stats ---")
print(f"Hamilton  |  Mean: {np.mean(ham_speed):.2f}  Max: {np.max(ham_speed):.2f}  Std Dev: {np.std(ham_speed):.2f}")
print(f"Russell   |  Mean: {np.mean(rus_speed):.2f}  Max: {np.max(rus_speed):.2f}  Std Dev: {np.std(rus_speed):.2f}")

# Basic stats for RPM
print("\n--- RPM Stats ---")
print(f"Hamilton  |  Mean: {np.mean(ham_rpm):.2f}  Max: {np.max(ham_rpm):.2f}")
print(f"Russell   |  Mean: {np.mean(rus_rpm):.2f}  Max: {np.max(rus_rpm):.2f}")

# Counting gear changes using np.diff
# np.diff gives the difference between each consecutive element
# if the gear changed, the difference won't be zero
ham_gears = np.array(engine_data1['nGear'])
rus_gears = np.array(engine_data2['nGear'])

ham_gear_changes = np.sum(np.diff(ham_gears) != 0)
rus_gear_changes = np.sum(np.diff(rus_gears) != 0)

print("\n--- Gear Changes ---")
print(f"Hamilton made {ham_gear_changes} gear changes on his fastest lap")
print(f"Russell  made {rus_gear_changes} gear changes on his fastest lap")

# Speed Delta using interpolation
# Both drivers have telemetry at slightly different distance points
# so we create a shared axis using np.linspace and then use np.interp
# to line both speed traces up before subtracting them
max_dist = min(engine_data1['Distance'].max(), engine_data2['Distance'].max())
common_distance = np.linspace(0, max_dist, 1000)

ham_speed_interp = np.interp(common_distance, engine_data1['Distance'], ham_speed)
rus_speed_interp = np.interp(common_distance, engine_data2['Distance'], rus_speed)

delta_speed = ham_speed_interp - rus_speed_interp  # positive = Hamilton faster at that point

print("\n--- Speed Delta (Hamilton - Russell) ---")
print(f"Max advantage Hamilton: {np.max(delta_speed):.1f} km/h")
print(f"Max advantage Russell:  {np.abs(np.min(delta_speed)):.1f} km/h")
print(f"Average delta:          {np.mean(delta_speed):.2f} km/h")

# Plotting the speed delta as an extra chart
fig2, ax5 = plt.subplots(figsize=(12, 3))
ax5.plot(common_distance, delta_speed, color='#E8B400', label='HAM - RUS')
ax5.axhline(0, color='white', linewidth=0.8, linestyle=':')
ax5.fill_between(common_distance, delta_speed, 0, where=(delta_speed > 0), alpha=0.3, color='#00A19B', label='Hamilton faster')
ax5.fill_between(common_distance, delta_speed, 0, where=(delta_speed < 0), alpha=0.3, color='#C0C0C0', label='Russell faster')
ax5.set_ylabel('Delta Speed (km/h)')
ax5.set_xlabel('Distance on Lap (m)')
ax5.set_title('Speed Delta: Hamilton - Russell (NumPy Interpolation)')
ax5.legend()
ax5.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()