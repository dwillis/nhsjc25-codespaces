#!/bin/bash

# Script to download WCS School Board Meeting Archives
# Years: 2005-2006 through 2024-2025

# Create output directory
OUTPUT_DIR="wcs_board_archives"
mkdir -p "$OUTPUT_DIR"

echo "Downloading WCS School Board Meeting Archives..."
echo "Output directory: $OUTPUT_DIR"
echo ""

# Counter for successful downloads
SUCCESS=0
FAILED=0

# Loop through years from 2005 to 2024
for year in {2005..2024}; do
    next_year=$((year + 1))
    
    # Format the year range (handle 2024-25 special case)
    if [ $year -eq 2024 ]; then
        year_range="${year}-2025"
    else
        year_range="${year}-${next_year}"
    fi
    
    # Construct URL
    url="https://docs.wcs.edu/pdf/boe/archives/${year_range}-School-Board-Meetings-Archive.pdf"
    
    # Output filename
    output_file="${OUTPUT_DIR}/${year_range}-School-Board-Meetings-Archive.pdf"
    
    echo "Attempting to download: $year_range"
    
    # Download with wget (using --spider first to check if file exists)
    if wget --spider -q "$url" 2>/dev/null; then
        wget -q -O "$output_file" "$url"
        if [ $? -eq 0 ]; then
            echo "  ✓ Successfully downloaded: $year_range"
            SUCCESS=$((SUCCESS + 1))
        else
            echo "  ✗ Failed to download: $year_range"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "  ✗ File not found: $year_range"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "Download complete!"
echo "Successful: $SUCCESS"
echo "Failed: $FAILED"
echo "Files saved to: $OUTPUT_DIR/"