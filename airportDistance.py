import json
from math import radians, sin, cos, sqrt, atan2

# Function to calculate the distance using Haversine formula
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers
    
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Difference in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c

# Load airport data
def load_airports():
    with open("airports.json", "r") as file:
        return json.load(file)

# Load aircraft data
def load_aircraft():
    with open("Aircraft_Specifications.json", "r") as file:
        return json.load(file)

# Get airport data by IATA code
def get_airport_by_iata(iata_code, airports_data):
    for airport in airports_data:
        if airport["IATA Code"] == iata_code:
            return airport
    return None

# Calculate adjusted range based on load percentage
def calculate_range_at_load(load_percentage, max_range):
    if load_percentage <= 80:
        return max_range
    else:
        # Adjust this constant for realism
        k = 0.0025  # Determines how quickly range decreases above 80%
        return max_range * (1 - k * (load_percentage - 80) ** 2)

# Find aircraft that can cover the distance and satisfy the load percentage
def find_aircraft_for_route(iata_code1, iata_code2, load_percentage):
    # Load airport and aircraft data
    airports = load_airports()
    aircraft = load_aircraft()

    # Get airport data by IATA codes
    airport1 = get_airport_by_iata(iata_code1, airports)
    airport2 = get_airport_by_iata(iata_code2, airports)

    if not airport1 or not airport2:
        return "One or both IATA codes are invalid."

    # Calculate distance between the two airports
    lat1, lon1 = airport1["Latitude"], airport1["Longitude"]
    lat2, lon2 = airport2["Latitude"], airport2["Longitude"]
    distance = haversine(lat1, lon1, lat2, lon2)
    print(f"Distance between {iata_code1} and {iata_code2}: {distance:.2f} km")

    # Find suitable aircraft
    suitable_aircraft = []
    for aircraft_info in aircraft:
        max_range = aircraft_info["Max Range (km)"]
        adjusted_range = calculate_range_at_load(load_percentage, max_range)
        if adjusted_range >= distance:
            suitable_aircraft.append({
                "Model Name and Variant": aircraft_info["Model Name and Variant"],
                "Adjusted Range (km)": adjusted_range
            })

    if suitable_aircraft:
        return suitable_aircraft
    else:
        return "No suitable aircraft found for this route."

# Example usage
iata_code1 = input("Input Departure IATA code: ")
iata_code2 = input("Input Destination IATA code: ")
load_percentage = float(input("Input Desired Load Percentage (0-100%): "))

available_aircraft = find_aircraft_for_route(iata_code1, iata_code2, load_percentage)
if isinstance(available_aircraft, list):
    print("\nAvailable Aircraft:")
    for aircraft in available_aircraft:
        print(f" - {aircraft['Model Name and Variant']} (Adjusted Range: {aircraft['Adjusted Range (km)']:.2f} km)")
else:
    print(available_aircraft)
