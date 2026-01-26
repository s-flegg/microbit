import pandas as pd
import matplotlib.pyplot as plt

columns = [
    "SkierID",
    "Time",
    "Temperature",
    "CO2",
    "Acceleration/g_force",
    "SessionID",
    "Warning"
]

df = pd.read_csv("dummy.csv", names=columns)
df.drop_duplicates()
print(df)

# Dataframe for Acceleration
df["SkierID"] = df["SkierID"].astype(str).str.strip()
df["Time"] = df["Time"].astype(str).str.strip()

# dummy conversions and parsing
df["SessionID"] = pd.to_numeric(df["SessionID"], errors="coerce")
df["Acceleration/g_force"] = pd.to_numeric(
    df["Acceleration/g_force"], errors="coerce")
df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

df = df.dropna(subset=["SkierID", "SessionID", "Time", "Acceleration/g_force"])
df = df.sort_values(["SkierID", "SessionID", "Time"])
df["t_sec"] = df.groupby(["SkierID", "SessionID"])["Time"].transform(
    lambda s: (s - s.iloc[0]).dt.total_seconds()
)
df["dt"] = df.groupby(["SkierID", "SessionID"])["t_sec"].diff().fillna(0)
df["speed"] = df.groupby(["SkierID", "SessionID"]).apply(
    lambda g: (g["Acceleration/g_force"] * g["dt"]).cumsum()
).reset_index(level=[0, 1], drop=True)

plt.figure()
for (skier, session), g in df.groupby(["SkierID", "SessionID"]):
    plt.plot(g["t_sec"], g["speed"], marker="o",
             label=f"{skier} Session {int(session)}")

plt.xlabel("Time in session (seconds)")
plt.ylabel("Speed (from integrating acceleration)")
plt.title("Speed over time for each session")
plt.legend()
plt.show()

# Dataframe for warnings
# do tmr
