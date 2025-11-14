"""Super simple scraper for Maryland Board of Physicians disciplinary alerts."""

from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

SOURCE_URL = "https://www.mbp.state.md.us/disciplinary.aspx"


# STEP 1: Download the web page so we can look at its HTML.
response = requests.get(SOURCE_URL, timeout=30)
response.raise_for_status()  # stop the script if the site is down
html = response.text

# STEP 2: Hand the HTML to BeautifulSoup so it becomes easy to search.
soup = BeautifulSoup(html, "html.parser")

# STEP 3: Find the table that lists the disciplinary alerts.
table = soup.find("table", class_="table")
if table is None:
    print("Could not find the alerts table. Maybe the page changed?")
    raise SystemExit(1)

# STEP 4: Pull out every table row (<tr>) that contains alert data.
if table.tbody:
    rows = table.tbody.find_all("tr")
else:
    rows = table.find_all("tr")

alerts = []

for row in rows:
    # Each row should have three columns: Name, Sanction, and Date.
    cells = row.find_all("td")
    if len(cells) < 3:
        continue  # skip header rows or anything unexpected

    # STEP 5: Read the text out of each column.
    name_link = cells[0].find("a")
    name = name_link.get_text(strip=True) if name_link else cells[0].get_text(strip=True)
    pdf = urljoin(SOURCE_URL, name_link["href"]) if name_link else ""
    sanction = cells[1].get_text(strip=True)
    date = cells[2].get_text(strip=True)

    alerts.append({"name": name, "sanction": sanction, "date": date, "pdf": pdf})

# STEP 6: Print everything in a friendly format.
print(f"Found {len(alerts)} alerts:")
for alert in alerts:
    print(f"- {alert['name']} ({alert['date']})")
    print(f"  Sanction: {alert['sanction']}")
    if alert["pdf"]:
        print(f"  Order: {alert['pdf']}")
