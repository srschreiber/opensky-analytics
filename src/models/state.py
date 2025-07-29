"""
The states property is a two-dimensional array. Each row represents a state vector and contains the following fields:

Index

Property

Type

Description

0

icao24

string

Unique ICAO 24-bit address of the transponder in hex string representation.

1

callsign

string

Callsign of the vehicle (8 chars). Can be null if no callsign has been received.

2

origin_country

string

Country name inferred from the ICAO 24-bit address.

3

time_position

int

Unix timestamp (seconds) for the last position update. Can be null if no position report was received by OpenSky within the past 15s.

4

last_contact

int

Unix timestamp (seconds) for the last update in general. This field is updated for any new, valid message received from the transponder.

5

longitude

float

WGS-84 longitude in decimal degrees. Can be null.

6

latitude

float

WGS-84 latitude in decimal degrees. Can be null.

7

baro_altitude

float

Barometric altitude in meters. Can be null.

8

on_ground

boolean

Boolean value which indicates if the position was retrieved from a surface position report.

9

velocity

float

Velocity over ground in m/s. Can be null.

10

true_track

float

True track in decimal degrees clockwise from north (north=0°). Can be null.

11

vertical_rate

float

Vertical rate in m/s. A positive value indicates that the airplane is climbing, a negative value indicates that it descends. Can be null.

12

sensors

int[]

IDs of the receivers which contributed to this state vector. Is null if no filtering for sensor was used in the request.

13

geo_altitude

float

Geometric altitude in meters. Can be null.

14

squawk

string

The transponder code aka Squawk. Can be null.

15

spi

boolean

Whether flight status indicates special purpose indicator.

16

position_source

int

Origin of this state’s position.

0 = ADS-B

1 = ASTERIX

2 = MLAT

3 = FLARM

17

category

int

Aircraft category.

0 = No information at all

1 = No ADS-B Emitter Category Information

2 = Light (< 15500 lbs)

3 = Small (15500 to 75000 lbs)

4 = Large (75000 to 300000 lbs)

5 = High Vortex Large (aircraft such as B-757)

6 = Heavy (> 300000 lbs)

7 = High Performance (> 5g acceleration and 400 kts)

8 = Rotorcraft

9 = Glider / sailplane

10 = Lighter-than-air

11 = Parachutist / Skydiver

12 = Ultralight / hang-glider / paraglider

13 = Reserved

14 = Unmanned Aerial Vehicle

15 = Space / Trans-atmospheric vehicle

16 = Surface Vehicle – Emergency Vehicle

17 = Surface Vehicle – Service Vehicle

18 = Point Obstacle (includes tethered balloons)

19 = Cluster Obstacle

20 = Line Obstacle

"""

# Maps the state 2-d Array into a structured object
from typing import List, Optional, Union
from pydantic import BaseModel, Field

from pydantic import BaseModel, Field
from typing import List, Optional, Union
import requests


class StateVector(BaseModel):
    icao24: Optional[str]
    callsign: Optional[str]
    origin_country: Optional[str]
    time_position: Optional[int]
    last_contact: Optional[int]
    longitude: Optional[float]
    latitude: Optional[float]
    baro_altitude: Optional[float]
    on_ground: Optional[bool]
    velocity: Optional[float]
    true_track: Optional[float]
    vertical_rate: Optional[float]
    sensors: Optional[List[int]]
    geo_altitude: Optional[float]
    squawk: Optional[str]
    spi: Optional[bool]
    position_source: Optional[int]
    #category: Optional[int]


class OpenSkyResponse(BaseModel):
    time: int
    states: map[str, StateVector]


def get_current_data() -> OpenSkyResponse:
    field_names = list(StateVector.__annotations__.keys())
    resp = requests.get("https://opensky-network.org/api/states/all")
    data = resp.json()

    if "states" not in data:
        raise ValueError("Invalid response format: 'states' key not found")
    
    raw_states = data.get("states", [])
    
    structured_states = {}

    for state in raw_states:
        if len(state) != len(field_names):
            raise ValueError(f"State vector length mismatch: expected {len(field_names)}, got {len(state)}")
        
        state_data = {field: value for field, value in zip(field_names, state)}
        structured_states[state_data["icao24"]] = StateVector(**state_data)

    if "time" not in data:
        raise ValueError("Invalid response format: 'time' key not found")

    return OpenSkyResponse(time=data.get("time", 0), states=structured_states)


if __name__ == "__main__":
    try:
        response = get_current_data()
    except Exception as e:
        print(f"An error occurred: {e}")