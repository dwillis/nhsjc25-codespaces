#!/bin/bash

# Simple analysis tasks for Maryland Board of Education payments data using csvkit

echo "=== Analysis 1: Count payments by Agency ==="
echo "Top 10 agencies by number of payments:"
csvcut -c "Agency Name" md_boe.csv | tail -n +2 | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Analysis 2: Summary statistics for payment amounts ==="
echo "Statistics for the Amount column:"
csvstat -c "Amount" md_boe.csv
echo ""

echo "=== Analysis 3: Top 10 payees by total amount ==="
echo "Filtering to see which organizations received the most money:"
csvsort -c "Amount" -r md_boe.csv | csvcut -c "Fiscal Year","Payee Name","Amount","Agency Name" | head -11
