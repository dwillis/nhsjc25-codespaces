"""Very small scraper that saves WV high school football scores to CSV."""

import csv
from pathlib import Path

import requests
from bs4 import BeautifulSoup

URL = "http://wvtailgatecentral.com/hs/fb2025/week_schedule.php?startdate=2025-11-04&enddate=2025-11-10"
OUTPUT_CSV = Path("wv_scores_week11.csv")

# Some small websites block the default Python requests user agent.
# Pretend to be a normal browser so the server is happy.
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}


# STEP 1: Download the page so we can read its HTML.
print("Downloading page...")
response = requests.get(URL, timeout=30, headers=HEADERS)

try:
    response.raise_for_status()  # stop if the request failed
except requests.HTTPError as exc:
    print("The website would not let us download the page. Try running the script again in a few minutes.")
    raise SystemExit(exc)
html = response.text

# STEP 2: Hand the HTML to BeautifulSoup for easy searching.
soup = BeautifulSoup(html, "html.parser")

# STEP 3: Grab the results table that lists every game.
table = soup.find("table")
if table is None:
    raise SystemExit("Could not find the results table on the page.")

rows = table.find_all("tr")
header = rows[0]
data_rows = rows[1:]  # skip the header row that contains column titles

# Helper to turn score text into an integer for math; blank cells become 0.
def parse_score(value: str) -> int:
    try:
        return int(value)
    except ValueError:
        return 0


# STEP 4: Pull the date, teams, scores, notes, and score differences from each row.
games = []
for row in data_rows:
    cells = row.find_all("td")
    if len(cells) < 7:
        continue  # skip anything that doesn't have all the cells we need

    game_date = cells[0].get_text(strip=True)
    away_team = cells[1].get_text(strip=True)
    away_score = cells[2].get_text(strip=True)
    home_team = cells[3].get_text(strip=True)
    home_score = cells[4].get_text(strip=True)
    note = cells[6].get_text(strip=True)

    # Figure out the absolute difference between the two scores.
    score_diff = abs(parse_score(away_score) - parse_score(home_score))

    games.append([game_date, away_team, away_score, home_team, home_score, note, score_diff])

print(f"Found {len(games)} games. Writing them to {OUTPUT_CSV}...")

# STEP 5: Save the rows to a CSV file.
with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(["date", "away_team", "away_score", "home_team", "home_score", "note", "score_diff"])
    writer.writerows(games)

print("All done! Open the CSV in Excel or Sheets to see the results.")
