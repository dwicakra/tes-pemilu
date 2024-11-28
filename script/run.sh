#!/bin/bash

echo "Starting data scraping process..."

# Run pkwkp scraper
echo "Scraping DISTRICT data..."
python scrap-district.py

# Run pkwkp scraper
echo "Scraping PKWKP data..."
python scrap-pkwkp.py

# Run pkwkp district scraper
echo "Scraping PKWKP district data..."
python scrap-pkwkp-district.py

# Run pkwkk scraper
echo "Scraping PKWKK data..."
python scrap-pkwkk.py

# Run pkwkk district scraper
echo "Scraping PKWKK district data..."
python scrap-pkwkk-district.py

# Run compiler
echo "Compiling data..."
python compiler.py

echo "All scraping tasks completed!"
