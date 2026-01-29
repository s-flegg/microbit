import pandas as pd
import matplotlib.pyplot as plt


def convert_file():

    character_list = []
    data = input("Enter file name: ").replace(
        " ", "").strip().lower()

    # File extention will be added or changed to .csv
    for i in data:
        if i == ".":
            break
        else:
            character_list.append(i)
    character_list.append(".csv")
    file_name = "".join(character_list)

    return file_name

# converting data types, cases, etc
# removing whitespaces
# changing none values into actual NaN
# dropping rows which dont have values in needed columns


def clean(df):
    df = df.copy()
    df.columns = df.columns.str.strip()
    df["SkierID"] = df["SkierID"].astype(str).str.strip()
    df["Type"] = df["Type"].astype(str).str.strip().str.upper()
    df["Time"] = pd.to_numeric(df["Time"], errors="coerce")
    df["Level"] = pd.to_numeric(df["Level"], errors="coerce")
    df["SessionID"] = pd.to_numeric(df["SessionID"], errors="coerce")
    df["Acceleration"] = pd.to_numeric(df["Acceleration"], errors="coerce")
    df["Warning"] = df["Warning"].astype(str).str.strip()
    df.loc[df["Warning"].str.upper().isin(
        ["NONE", "NAN", "", "N"]), "Warning"] = pd.NA
    df = df.dropna(subset=["SkierID", "Type", "Time"])
    print(df)
    return df


def acceleration(df):
    adf = df[df["Type"] == "ACCEL"].copy()

    # removing rows w/o sessionID and acceleration
    adf = adf.dropna(subset=["SessionID", "Acceleration"])
    adf = adf.sort_values(["SkierID", "SessionID", "Time"])
    adf["dt"] = adf.groupby(["SkierID", "SessionID"])["Time"].diff().fillna(0)

    adf["dt"] = pd.to_numeric(adf["dt"], errors="coerce")
    df["Acceleration"] = pd.to_numeric(df["Acceleration"], errors="coerce")
    adf = adf.dropna(subset=["Acceleration", "dt"])

    # change in speed over time
    adf["speed"] = (adf["Acceleration"] * adf["dt"]
                    ).groupby([adf["SkierID"], adf["SessionID"]]).cumsum()

    plt.figure()
    for (skier, session), g in adf.groupby(["SkierID", "SessionID"]):
        plt.plot(g["Time"], g["speed"], color="blue", marker=".",
                 label=f"{skier} Session {int(session)}")
    plt.xlabel("Elapsed time in seconds")
    plt.ylabel("Speed (m/s)")
    plt.title("Speed over time for each session")
    # plt.legend()
    plt.grid(True)
    plt.show()


def CO2(df):
    cdf = df[df["Type"] == "CO2"].copy()

    # removing rows which dont have values in level
    cdf = cdf.dropna(subset=["Level"])

    plt.figure()
    plt.scatter(cdf["Time"], cdf["Level"],
                label="CO2 readings", color="red", marker=".")
    plt.axhline(y=1500, color="orange", linestyle="--",
                label="Danger threshold")
    plt.xlabel("Time")
    plt.ylabel("CO2 (ppm)")
    plt.title("CO2 levels over time")
    plt.legend()
    plt.grid(True)
    plt.show()


def temp(df):
    tdf = df[df["Type"] == "TEMP"].copy()

    # same idea as before, removing rows with no level
    tdf = tdf.dropna(subset=["Level"])

    plt.figure()
    plt.scatter(tdf["Time"], tdf["Level"], label="Temperature readings")
    plt.axhline(y=-10, linestyle="--", label="Danger threshold")
    plt.xlabel("Time")
    plt.ylabel("Temperature (Celsius)")
    plt.title("Temperature over time")
    plt.legend()
    plt.grid(True)
    plt.show()


while True:
    try:
        data = convert_file()
        df = pd.read_csv(data)
        break
    except FileNotFoundError:
        print("File not found. Please try again.")

while True:
    df = clean(df)
    try:
        print("1. Acceleration")
        print("2. CO2 Levels")
        print("3. Temperature Levels")
        print("4. Exit")
        user_input = int(input(": "))
        if user_input == 1:
            acceleration(df)
            break
        elif user_input == 2:
            CO2(df)
            break
        elif user_input == 3:
            temp(df)
            break
        elif user_input == 4:
            exit()
        else:
            print("Please choose between 1-4.")
    except ValueError:
        print("Please enter an integer between 1-4.")
