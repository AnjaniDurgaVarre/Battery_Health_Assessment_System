from flask import Flask, render_template, request, redirect
import os
import pandas as pd

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

battery_info = {}
vehicle_info = {}

battery_table = []
vehicle_table = []

selected_vehicle = None
allocated_battery = None


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- DATASET ----------------

@app.route("/dataset")
def dataset():
    return render_template(
        "dataset.html",
        battery_info=battery_info,
        vehicle_info=vehicle_info,
        battery_table=battery_table,
        vehicle_table=vehicle_table
    )


# ---------------- VEHICLE SEARCH PAGE ----------------

@app.route("/vehicle_search")
def vehicle_search():
    return render_template("vehicle_search.html", result=None)

# ---------------- RECOMMENDATION PAGE ----------------

@app.route("/recommendation")
def recommendation():

    global selected_vehicle
    global battery_table
    global allocated_battery

    recommended_battery = None

    if selected_vehicle:

        min_soc = selected_vehicle["minimum_acceptable_SOC_percent"]

        eligible_batteries = []

        for battery in battery_table:

            if (
                battery["station_status"] == "AVAILABLE"
                and battery["state_of_charge_percent"] >= min_soc
                and battery["state_of_health_percent"] >= 80
                and battery["temperature_C"] < 40
            ):
                eligible_batteries.append(battery)

        if eligible_batteries:

            for battery in eligible_batteries:

                battery["priority_score"] = (
                    battery["state_of_health_percent"] * 0.5 +
                    battery["state_of_charge_percent"] * 0.3 -
                    battery["temperature_C"] * 0.2
                )

            recommended_battery = max(
                eligible_batteries,
                key=lambda x: x["priority_score"]
            )

            allocated_battery = recommended_battery

    return render_template(
        "recommendation.html",
        vehicle=selected_vehicle,
        battery=recommended_battery
    )
# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    print("Battery Count =", len(battery_table))

    total = len(battery_table)

    available = 0
    allocated = 0
    maintenance = 0

    for battery in battery_table:

        status = battery["station_status"].upper()

        if status == "AVAILABLE":
            available += 1

        elif status == "ALLOCATED":
            allocated += 1

        else:
            maintenance += 1

    return render_template(
        "dashboard.html",
        total_batteries=total,
        available=available,
        allocated=allocated,
        maintenance=maintenance
    )
# ---------------- GRAPHS ----------------

@app.route("/graphs")
def graphs():

    global selected_vehicle
    global battery_table

    vehicle_soc = 0
    battery_soc = 0

    battery_ids = []
    battery_soh = []
    battery_temp = []

    available = 0
    allocated = 0
    maintenance = 0

    if selected_vehicle:
        vehicle_soc = selected_vehicle["minimum_acceptable_SOC_percent"]

    for battery in battery_table:

        battery_ids.append(str(battery["battery_id"]))
        battery_soh.append(battery["state_of_health_percent"])
        battery_temp.append(battery["temperature_C"])

        status = battery["station_status"].upper()

        if status == "AVAILABLE":
            available += 1

        elif status == "ALLOCATED":
            allocated += 1
            battery_soc = battery["state_of_charge_percent"]

        else:
            maintenance += 1

    return render_template(
        "graph.html",
        vehicle_soc=vehicle_soc,
        battery_soc=battery_soc,
        battery_ids=battery_ids,
        battery_soh=battery_soh,
        battery_temp=battery_temp,
        available=available,
        allocated=allocated,
        maintenance=maintenance
    )
# ---------------- UPLOAD BATTERY ----------------

@app.route("/upload_battery", methods=["POST"])
def upload_battery():

    global battery_info
    global battery_table

    file = request.files["battery_file"]

    if file.filename != "":

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)

        battery_info = {
            "filename": file.filename,
            "records": len(df)
        }

        battery_table = df.to_dict(orient="records")

    return redirect("/dataset")


# ---------------- UPLOAD VEHICLE ----------------

@app.route("/upload_vehicle", methods=["POST"])
def upload_vehicle():

    global vehicle_info
    global vehicle_table

    file = request.files["vehicle_file"]

    if file.filename != "":

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        df = pd.read_csv(filepath)

        vehicle_info = {
            "filename": file.filename,
            "records": len(df)
        }

        vehicle_table = df.to_dict(orient="records")

    return redirect("/dataset")


# ---------------- SEARCH VEHICLE ----------------

@app.route("/search_vehicle", methods=["POST"])
def search_vehicle():

    global selected_vehicle

    vehicle_id = request.form["vehicle_id"].strip().upper()

    result = None

    for vehicle in vehicle_table:

       if str(vehicle["request_id"]).upper() == vehicle_id:

           result = vehicle

           selected_vehicle = vehicle

           break

    return render_template(
        "vehicle_search.html",
        result=result
    )

# ---------------- ALLOCATE BATTERY ----------------

@app.route("/allocate_battery")
def allocate_battery():

    global battery_table
    global selected_vehicle
    global allocated_battery

    if selected_vehicle is None:
        return redirect("/vehicle_search")

    min_soc = selected_vehicle["minimum_acceptable_SOC_percent"]

    eligible_batteries = []

    for battery in battery_table:

        if (
            battery["station_status"] == "AVAILABLE"
            and battery["state_of_charge_percent"] >= min_soc
            and battery["state_of_health_percent"] >= 80
            and battery["temperature_C"] < 40
        ):

            battery["priority_score"] = (
                battery["state_of_health_percent"] * 0.5 +
                battery["state_of_charge_percent"] * 0.3 -
                battery["temperature_C"] * 0.2
            )

            eligible_batteries.append(battery)

    if eligible_batteries:

        allocated_battery = max(
            eligible_batteries,
            key=lambda x: x["priority_score"]
        )

        allocated_battery["station_status"] = "ALLOCATED"

    return redirect("/dashboard")
    # ---------------- REPORTS ----------------

@app.route("/reports")
def reports():
    global allocated_battery

    total = len(battery_table)

    available = 0
    allocated = 0
    maintenance = 0

  

    for battery in battery_table:

        status = battery["station_status"].upper()

        if status == "AVAILABLE":
            available += 1

        elif status == "ALLOCATED":
            allocated += 1


        else:
            maintenance += 1

    return render_template(
        "report.html",
        total=total,
        available=available,
        allocated=allocated,
        maintenance=maintenance,
        vehicle=selected_vehicle,
        battery=allocated_battery
    )
# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)