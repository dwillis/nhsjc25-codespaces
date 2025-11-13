#!/bin/bash

# Load CSV into SQLite database and view with Datasette

# Create/overwrite the database
echo "Loading md_boe.csv into SQLite database..."
sqlite-utils insert md_boe.db payments md_boe.csv --csv

echo "Database created successfully!"
echo ""
echo "Starting Datasette server..."
echo "The database will be available in your browser"
echo "Press Ctrl+C to stop the server"
echo ""

# Start datasette (will open in browser if possible)
datasette md_boe.db --open
