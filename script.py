import requests
import xml.etree.ElementTree as ET
from datetime import date

# Fetch data from NationStates API
headers = {
    'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'  
}
nation = "athretvari"  # Replace with nation's name
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
# NationStates Report for {nation}

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
    # Save the Markdown content to a file
    with open(f'./reports/report_{nation}.md', 'w') as file:
        file.write(md_content)
else:
    print("Failed to fetch data from NationStates API.")
