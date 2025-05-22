# Pinterest Engagement Analytics CLI

A Python-based command-line interface (CLI) tool to analyze Pinterest-style engagement trends. Built with SQLite and Matplotlib, this tool lets you process a dataset of posts, load it into a local database, and perform various analytics on likes and comments.

## Features

- 📥 Load Pinterest post data from a CSV file into a SQLite database
- 🔍 View sample data rows from the database
- 🔢 Identify the top 5 most engaging posts by likes or comments
- 📊 Visualize top posts with horizontal bar charts

## Technologies Used
- Python 3
- SQLite3
- Matplotlib
- CSV file processing

## CSV Format

The tool expects a CSV file named `pinterest_data.csv` in the following format:

```csv
title,author,likes,comments,category
"Post 1","Author A",124,45,"Travel"
"Post 2","Author B",300,120,"Food"
...
