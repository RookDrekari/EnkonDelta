import requests
import xml.etree.ElementTree as ET
from datetime import date

# Fetch data from NationStates API
def fetch_census_report(nation):
    headers = {
        'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'  
    }
    url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region+population+currency+animal"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the XML data
        root = ET.fromstring(response.content)
        region = root.find('REGION').text
        population = root.find('POPULATION').text
        currency = root.find('CURRENCY').text
        animal = root.find('ANIMAL').text

        # Get today's date
        reportDate = date.today()

        # Generate Markdown content
        md_content = f"""
# Census Report for {nation.title()}

## Region
**{region}**

## Population
**{population}**

## Currency
**{currency}**

## Animal
**{animal}**

---

*Data fetched from the NationStates API.*
*This report was generated on {reportDate}*
"""
        # Save the Markdown content to a file in the reports folder
        with open(f'./reports/report_{nation}.md', 'w') as file:
            file.write(md_content)

    else:
        print(f"Failed to fetch data for {nation}. Status code: {response.status_code}")

# Read the list of nations from a file
with open('nations.txt', 'r') as file:
    nations = [line.strip() for line in file.readlines()]

# Generate a report for each nation
for nation in nations:
    fetch_census_report(nation)
