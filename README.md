# dataops-scheduled-bus-trips
 > Scheduled Bus Trips from GTFS with extra computed fields including scheduled start time

## background
We are trying build a GTFS Realtime feed by combining the data from our implementation of Clever's Bus Time API, our static GTFS data, and other data feeds.  Clever uses a different trip id from our static GTFS, so we needed a dataset the included extra information like the scheduled start time in order to match the two data sources.

## frequency
The pipeline automatically runs once a day to make sure we are in sync, but the underlying data only changes every several months.

## columns
| column | example | description |
| :--- | :--- | :--- |
| **trip_id** | `1009020` | The unique identifier of the stop in our static GTFS data. |
| **route_id** | `"4"` | The name of the route. |
| **route_short_name** | `"4"` | Same as route_id. |
| **route_long_name** | `"Eastgate/Hamilton Pl"` | Longer name for the route |
| **route_type** | `"3"` | not sure |
| **route_color** | `"00aeef"` | Color for the route for display purposes |
| **route_text_color** | `"000000"` | Text color for the route for display purposes |
| **service_id** | `"2"` | Which type of service (e.g., weekday, Saturday, or Sunday) |
| **service_monday** | `true` | if the trip runs on Monday |
| **service_tuesday** | `true` | if the trip runs on Tuesday |
| **service_wednesday** | `true` | if the trip runs on Wednesday |
| **service_thursday** | `true` | if the trip runs on Thursday |
| **service_friday** | `true` | if the trip runs on Friday |
| **service_saturday** | `false` | if the trip runs on Saturday |
| **service_sunday** | `false` | if the trip runs on Sunday |
| **service_start_date** | `"20250817"` | the first daty the trip runs |
| **service_end_date** | `"20260509"` | the last day the trip runs |
| **headsign** | `"DOWNTOWN"` | the headsign (what displays on the outward-facing bus sign) |
| **start_time** | `"15:15:00"` | when the trip is supposed to begin (in 24-hr time) |
| **end_time** | `"16:15:00"` | when the trip is supposed to end (in 24-hr time) |
| **direction_id** | `"16:15:00"` | numerical identifier for the direction |
| **direction** | `"Inbound"` | CARTA-specific direction definition (e.g. "Inbound" or "Outbound") |
| **direction** | `"Inbound"` | CARTA-specific direction definition (e.g. "Inbound" or "Outbound") |
| **block_id** | `"6302"` | GTFS Block ID |
| **shape_id** | `"shp-4-64"` | GTFS Shape ID |
| **wheelchair_accessible** | `true` | Wheelchair Accessible |
| **bikes_allowed** | `true` | Bikes are allowed on the trip |

## download links
- [metadata](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_bus_trips/v1/meta.json)
- [csv](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_bus_trips/v1/data.csv)
- [parquet](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_bus_trips/v1/data.parquet)
- [json](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_bus_trips/v1/data.json)
- [json lines](https://gocarta.s3.us-east-2.amazonaws.com/public/data/scheduled_bus_trips/v1/data.jsonl)

## preview links
- You can query the data with SQL using [duckdb](https://shell.duckdb.org/#queries=v0,CREATE-TABLE-dataset-AS-SELECT-*-FROM-'s3://gocarta/public/data/scheduled_bus_trips/v1/data.parquet'~,Describe-dataset~).

## support
Post an issue [here](https://github.com/gocarta/dataops-scheduled-bus-trips/issues) or email the package author at DanielDufour@gocarta.org.
