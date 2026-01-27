import pandas as pd
import matplotlib.pyplot as plt

columns = [
    "SkierID",
    "Time",
    "Temperature",
    "CO2",
    "Elapsed_Time",
    "Acceleration/g_force",
    "SessionID",
    "Warning"
]

df = pd.read_csv("dummy.csv", names=columns)
df.drop_duplicates()
# print(df)

# DATAFRAME FOR ACCELERATION

# dummy conversions and parsing
df["SkierID"] = df["SkierID"].astype(str).str.strip()
df["Time"] = df["Time"].astype(str).str.strip()
df["SessionID"] = pd.to_numeric(df["SessionID"], errors="coerce")
df["Acceleration/g_force"] = pd.to_numeric(
    df["Acceleration/g_force"], errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
df["Elapsed_Time"] = df["Elapsed_Time"].astype(str).str.strip()
df["Elapsed_Time"] = pd.to_datetime(df["Elapsed_Time"], errors="coerce")

df = df.dropna(subset=["SkierID", "SessionID", "Time", "Acceleration/g_force"])
df = df.sort_values(["SkierID", "SessionID", "Time"])
df["dt"] = df.groupby(["SkierID", "SessionID"])["Elapsed_Time"].diff().fillna(0)
df["speed"] = df.groupby(["SkierID", "SessionID"]).apply(
    lambda g: (g["Acceleration/g_force"] * g["dt"]).cumsum()
).reset_index(level=[0, 1], drop=True)

plt.figure()
for (skier, session), g in df.groupby(["SkierID", "SessionID"]):
    plt.plot(g["Elapsed_Time"], g["speed"], marker="o",
    label=f"{skier} Session {int(session)}")

# Elapsed time
plt.xlabel("Time in session (seconds)")

# time x accel
plt.ylabel("Speed (from integrating acceleration)")
plt.title("Speed over time for each session")
plt.legend()
plt.show()

# DATAFRAME FOR WARNINGS

# CO2
co2_warnings = df[df["Warning"] == "CO2"]

plt.figure() # figsize=(10, 5)
plt.scatter(
co2_warnings["Time"],
co2_warnings["CO2"],
color="red",
label="Dangerous CO2 Event")

plt.axhline(y=1500, color="orange", linestyle="--", label="Danger Threshold")
plt.xlabel("Time")
plt.ylabel("CO2 Level (ppm)")
plt.title("Dangerous CO2 Levels Detected Over Time")
plt.legend()
plt.grid(True)
# plt.show()

# TEMP
temp_warnings = df[df["Warning"] == "TEMP"]

plt.figure(figsize=(10, 5))
plt.scatter(
    temp_warnings["Time"],
    temp_warnings["Temperature"],
    color="blue",
    label="Temperature Warning"
)

plt.axhline(y=-10, color="red", linestyle="--", label="Danger Threshold")

plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Dangerous Temperature Events Over Time")
plt.legend()
plt.grid(True)

# plt.show()
