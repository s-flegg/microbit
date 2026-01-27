import pandas as pd
import matplotlib.pyplot as plt

columns = [
    "SkierID",
    "Type",
    "Time",
    "Level",
    "Warning",
    "SessionID",
    "Acceleration",
]

df = pd.read_csv("dummy.csv", names=columns)
# print(df)

# ACCELERATION
df["SkierID"] = df["SkierID"].astype(str).str.strip()
df["Type"] = df["Type"].astype(str).str.strip()
df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
df["SessionID"] = pd.to_numeric(df["SessionID"], errors="coerce")
df["Acceleration"] = pd.to_numeric(df["Acceleration"], errors="coerce")
df = df.dropna(subset=["SkierID", "SessionID", "Time", "Acceleration"])
df = df[df["Type"] == "accel"]
df = df.sort_values(["SkierID", "SessionID", "Time"])
df["dt"] = df.groupby(["SkierID", "SessionID"])["Time"].diff().fillna(0)
df["speed"] = (
    df["Acceleration"] * df["dt"]
).groupby([df["SkierID"], df["SessionID"]]).cumsum()

plt.figure()
for (skier, session), g in df.groupby(["SkierID", "SessionID"]):
    plt.plot(g["Time"], g["speed"], marker="o",
             label=f"{skier} Session {int(session)}")

plt.xlabel("Elapsed time in session (seconds)")
plt.ylabel("Speed (m/s)")
plt.title("Speed over time for each session")
plt.legend()
plt.show()

# CO2
# co2_warnings = df[df["Warning"] == "CO2"]
co2_levels = df[df["Type"] == "CO2"]

plt.figure(figsize=(10, 5))
plt.scatter(
    co2_levels["Time"],
    co2_levels["CO2"],
    color="red",
    label="CO2 Events")
plt.axhline(y=1500, color="orange", linestyle="--", label="Danger Threshold")
plt.xlabel("Time")
plt.ylabel("CO2 Level (ppm)")
plt.title("CO2 Levels Detected Over Time")
plt.legend()
plt.grid(True)
# plt.show()
# ^ works

# TEMP
# maybe integrate temp and co2 together?
temp_warnings = df[df["Warning"] == "TEMP"]
temp_levels = df[df["Type"] == "TEMP"]

plt.figure(figsize=(10, 5))
plt.scatter(
    temp_levels["Time"],
    temp_levels["Temperature"],
    color="blue",
    label="Temperature Levels"
)
plt.axhline(y=-10, color="red", linestyle="--", label="Danger Threshold")
plt.xlabel("Time")
plt.ylabel("Temperature (°C)")
plt.title("Dangerous Temperature Events Over Time")
plt.legend()
plt.grid(True)
# plt.show()
# ^ works
