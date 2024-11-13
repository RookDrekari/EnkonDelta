import requests
import xml.etree.ElementTree as ET

# Fetch data from NationStates API
headers = {
    'User-Agent': 'EnkonDelta (Contact: https://www.nationstates.net/nation=nedea)'  # Replace with your app name and contact info
}
nation = "nedea"  # Replace with your nation's name
url = f"https://www.nationstates.net/cgi-bin/api.cgi?nation={nation}&q=region+population"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Parse the XML data
    root = ET.fromstring(response.content)
    region = root.find('REGION').text
    population = root.find('POPULATION').text

    # Generate Markdown content
    md_content = f"""
# NationStates Report for {nation}

## Region
**{region}**

## Population
**{population}**

---

*Data fetched from the NationStates API.*
"""
    # Save the Markdown content to a file
    with open('nation_report.md', 'w') as file:
        file.write(md_content)
else:
    print("Failed to fetch data from NationStates API.")
