import requests
import xml.etree.ElementTree as ET
from datetime import date
import yaml
import os
import re

# Predefined census IDs for industries
CENSUS_IDS = {
    "Automobile Manufacturing": 10,
    "Cheese Exports": 11,
    "Basket Weaving": 12,
    "Information Technology": 13,
    "Pizza Delivery": 14,
    "Trout Fishing": 15,
    "Arms Manufacturing": 16,
    "Beverage Sales": 18,
    "Timber Wood Chipping": 19,
    "Mining": 20,
    "Insurance": 21,
    "Furniture Restoration": 22,
    "Retail": 23,
    "Book Publishing": 24,
    "Gambling": 25
}


def fetch_census_report(nation):
    headers = {
        'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'  
    }

    # Add census IDs to the query
    census_query = '+'.join(str(id) for id in CENSUS_IDS.values())
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region+population+currency+animal+census;scale={census_query}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the XML data
        root = ET.fromstring(response.content)
        new_data = {
            "nation": nation.title(),
            "region": root.find('REGION').text,
            "population": int(root.find('POPULATION').text),
            "currency": root.find('CURRENCY').text,
            "animal": root.find('ANIMAL').text,
            "industries": {}
        }

        # Extract industry data
        for industry, id in CENSUS_IDS.items():
            value = root.find(f".//SCALE[@id='{id}']/SCORE").text
            new_data["industries"][industry] = float(value)  # Convert to float for precision

        # Add report date
        report_date = date.today()

        # Load existing data, strip comments
        file_path = f'./data/reports/report_{nation}.yaml'
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()
                # Remove comments
                content_no_comments = re.sub(r'#.*', '', content)
                existing_data = yaml.safe_load(content_no_comments) or {}
        else:
            existing_data = {}

        # Merge new data with existing data
        merged_data = {**existing_data, **new_data}

        # Generate YAML with single comment
        yaml_content = yaml.dump(merged_data, default_flow_style=False)
        yaml_content += f"\n# Report generated on {report_date}\n"

        # Save to file
        with open(file_path, 'w') as file:
            file.write(yaml_content)

    else:
        print(f"Failed to fetch data for {nation}. Status code: {response.status_code}")

# Read the list of nations from a file
with open('nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

# Generate a report for each nation
for nation in nations:
    fetch_census_report(nation)
