# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "datablob",
#     "requests",
#     "simple-env",
# ]
# ///
from collections import defaultdict
import csv
import datablob
import io
import requests
import simple_env as se
import zipfile

AWS_BUCKET_NAME = se.get("AWS_BUCKET_NAME")
AWS_BUCKET_PATH = se.get("AWS_BUCKET_PATH")

# load static gtfs data that doesn't change often into memory
GTFS_URL = (
    "https://raw.githubusercontent.com/gocarta/gtfs/refs/heads/master/gtfs_current.zip"
)

response = requests.get(GTFS_URL)
zip_data = io.BytesIO(response.content)

trip_stop_times = defaultdict(list)
trip_scheduled_start_times = {}
trip_scheduled_end_times = {}

calendar = {}
routes = {}

bikes_allowed = {
    "0": None,  # unknown
    "1": True,
    "2": False,
}

direction_id = {"0": "Outbound", "1": "Inbound"}

wheelchair_accessible = {
    "0": None,  # unknown
    "1": True,
    "2": False,
}

results = []

with zipfile.ZipFile(zip_data) as z:
    with z.open("calendar.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            calendar[row["service_id"]] = row

    with z.open("routes.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            routes[row["route_id"]] = row

    with z.open("stop_times.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            trip_stop_times[row["trip_id"]].append(row)

    # calculate the scheduled start time and end time for each trip
    for trip_id, stop_times in trip_stop_times.items():
        stop_times_sorted = sorted(stop_times, key=lambda r: int(r["stop_sequence"]))
        trip_scheduled_start_times[trip_id] = stop_times_sorted[0]["departure_time"]
        trip_scheduled_end_times[trip_id] = stop_times_sorted[-1]["arrival_time"]

    with z.open("trips.txt") as f:
        for row in csv.DictReader(f.read().decode("utf-8-sig").splitlines()):
            trip_id = row["trip_id"]

            service_id = row["service_id"]
            cal = calendar[service_id]

            route_id = row["route_id"]
            route = routes[route_id]

            trip = {
                "trip_id": trip_id,
                "route_id": route_id,
                "route_short_name": route["route_short_name"],
                "route_long_name": route["route_long_name"],
                "route_type": route["route_type"],
                "route_color": route["route_color"],
                "route_text_color": route["route_text_color"],
                "service_id": service_id,
                "service_monday": cal["monday"] == "1",
                "service_tuesday": cal["tuesday"] == "1",
                "service_wednesday": cal["wednesday"] == "1",
                "service_thursday": cal["thursday"] == "1",
                "service_friday": cal["friday"] == "1",
                "service_saturday": cal["saturday"] == "1",
                "service_sunday": cal["sunday"] == "1",
                "service_start_date": cal["start_date"],
                "service_end_date": cal["end_date"],
                "headsign": row["trip_headsign"],
                "start_time": trip_scheduled_start_times[trip_id],
                "end_time": trip_scheduled_end_times[trip_id],
                "direction_id": direction_id[row["direction_id"]],
                "block_id": row["block_id"],
                "shape_id": row["shape_id"],
                "wheelchair_accessible": wheelchair_accessible[
                    row["wheelchair_accessible"]
                ],
                "bikes_allowed": bikes_allowed[row["bikes_allowed"]],
            }

            results.append(trip)

client = datablob.DataBlobClient(
    bucket_name=AWS_BUCKET_NAME, bucket_path=AWS_BUCKET_PATH
)

client.update_dataset(
    name="scheduled_bus_trips",
    description="Scheduled Bus Trips from GTFS with extra computed fields including scheduled start time and end time",
    version="1",
    data=results,
    column_names=[
        "trip_id",
        "route_id",
        "route_short_name",
        "route_long_name",
        "route_type",
        "route_color",
        "route_text_color",
        "service_id",
        "service_monday",
        "service_tuesday",
        "service_wednesday",
        "service_thursday",
        "service_friday",
        "service_saturday",
        "service_sunday",
        "service_start_date",
        "service_end_date",
        "headsign",
        "start_time",
        "end_time",
        "direction_id",
        "block_id",
        "shape_id",
        "wheelchair_accessible",
        "bikes_allowed",
    ],
)

print(f"[dataops-scheduled-bus-trips] updated {len(results)} rows")
