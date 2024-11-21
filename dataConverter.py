import csv
import json

# Function to parse the .dat file and convert it to JSON
def parse_dat_to_json(dat_file_path, output_json_path):
    airports = []
    with open(dat_file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) < 8:
                continue
            
            # Extract the relevant fields
            airport_name = row[1].strip('"')
            city = row[2].strip('"')
            country = row[3].strip('"')
            iata_code = row[4].strip('"')
            latitude = float(row[6])
            longitude = float(row[7])

            # Append the structured data to the list
            airports.append({
                "Airport Name": airport_name,
                "City": city,
                "Country": country,
                "IATA Code": iata_code,
                "Latitude": latitude,
                "Longitude": longitude
            })

    # Write the JSON data to a file
    with open(output_json_path, "w") as json_file:
        json.dump(airports, json_file, indent=4)

# Example usage
dat_file = "airports.dat"  # Path to your .dat file
output_json = "airports.json"
parse_dat_to_json(dat_file, output_json)
print(f"Data converted and saved to {output_json}")
