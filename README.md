# nhsjc25-codespaces
Materials for a presentation at the Fall 2025 National High School Journalism Convention

## Setup

Install the required dependencies:

```bash
pip install -r requirements.txt
datasette install datasette-codespaces
```

## Data

The repository includes `md_boe.csv`, which contains Maryland Board of Education payment data including fiscal year, agency name, payee information, payment amounts, and purposes.

## Scripts

### get_school_board_pdfs.sh
Downloads WCS School Board Meeting Archives PDFs from 2005-2006 through 2024-2025. Creates a `wcs_board_archives` directory and downloads all available meeting minutes.

### analyze_md_boe.sh
Performs three simple analysis tasks on the Maryland BOE payments data using csvkit:
- Counts payments by agency to show which school districts make the most payments
- Calculates summary statistics (min, max, mean, median) for payment amounts
- Displays the top 10 largest payments by amount

Run with:
```bash
./analyze_md_boe.sh
```

### load_and_view.sh
Loads the CSV data into a SQLite database and launches an interactive Datasette web interface for browsing and querying the data.

Run with:
```bash
./load_and_view.sh
```

Press Ctrl+C to stop the Datasette server when finished.

### scrape_mbp_alerts.py
Downloads the current Maryland Board of Physicians disciplinary alerts table and prints each provider's name, sanction, date, and PDF order link.

Run with:
```bash
python scrape_mbp_alerts.py
```
