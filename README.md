
  F1 TELEMETRY ANALYSIS — EXPERIENTIAL LEARNING PROJECT
  Mercedes Teammate Comparison: Australia GP 2024


OVERVIEW
--------
This project uses real Formula 1 telemetry data to compare the
fastest laps of Lewis Hamilton and George Russell (Mercedes AMG)
at the 2024 Australian Grand Prix. It demonstrates practical data
analysis using three core Python libraries: NumPy, Pandas, and
Matplotlib, with F1 data accessed via the FastF1 library.


FILES IN THIS PROJECT
---------------------
main.py                 Main Python analysis script
cache_folder/           Auto-created on first run — stores downloaded
                        F1 session data so you don't re-download it
README.txt              This file


REQUIREMENTS
------------
Python 3.8+

Install dependencies using pip:

    pip install fastf1 pandas numpy matplotlib

FastF1 will automatically download the 2024 Australian GP session
on the first run and save it to cache_folder/ locally.


HOW TO RUN
----------
Recommended: run from Command Prompt outside VSCode for best speed.

1. Open Command Prompt
2. Navigate to the project folder:

       cd C:\F1

3. Run the script:

       python main.py

4. The dashboard (4 plots) will appear first.
   The NumPy stats will print to the terminal.
   The speed delta chart will appear after.

Note: Do NOT close the dashboard window mid-run — just let both
plot windows open on their own. The script uses block=False so
everything runs through without you needing to interact.


WHAT THE CODE DOES (STEP BY STEP)
----------------------------------
Step 1   Sets up a local cache folder to store downloaded data

Step 2   Loads the 2024 Australian GP race session via FastF1
         weather=False and messages=False speeds up the load
         by skipping data the project doesn't use

Step 3   Picks the single fastest lap for Hamilton and Russell
         from the full race — gives the cleanest comparison

Step 4   Extracts full telemetry for both laps using
         get_telemetry() which merges car data and GPS together

Step 5   Filters down to only the columns needed:
         Time, Distance, X, Y, Z, RPM, Speed, nGear, Throttle

Step 6   Builds a 4-panel Matplotlib dashboard:
           Panel 1 — Speed trace (km/h vs distance)
           Panel 2 — Engine RPM vs distance
           Panel 3 — Throttle percentage vs distance
           Panel 4 — Track map (GPS X/Y coordinates)
         sharex=True links all panels on the same distance axis

Step 7   Shows the dashboard with block=False so the script
         keeps running without waiting for the window to close

Step 8   NumPy analysis section:
           8a — Mean, max, std deviation for speed and RPM
           8b — Gear change count using np.diff()
           8c — Speed delta using np.linspace + np.interp
                to put both drivers on a common distance axis
           8d — Plots the speed delta with fill_between()
                showing exactly where each driver was faster


LIBRARY ROLES
-------------
NumPy      Statistical calculations (mean, max, std deviation),
           gear change detection via np.diff(), shared distance
           axis via np.linspace(), speed resampling via np.interp()

Pandas     Session loading, lap filtering (pick_drivers,
           pick_fastest), telemetry DataFrame management
           and column selection

Matplotlib 4-panel telemetry dashboard with sharex=True,
           speed delta chart with fill_between() shading,
           GPS track map overlay

FastF1     F1 data API — provides access to official timing,
           telemetry and positional data for any session


KNOWN BEHAVIOURS
----------------
- First run is slower (downloading session data from internet)
- Subsequent runs are fast (reading from local cache)
- Both plot windows open together and stay open until closed
- session.load() may still take 30-60 seconds on first run
  depending on internet speed — this is normal


