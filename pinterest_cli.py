"""
Pinterest Engagement CLI Tool

Analyze Pinterest-style engagement data using a command-line interface.
This tool loads data from a CSV into an SQLite database and helps users explore
and visualize posts with the most likes or comments.

Developed by: Dunya Rahim
Date: Dec. 2024 – Feb. 2025
"""

import sqlite3
import csv
import matplotlib.pyplot as plt
import os

DB_NAME = 'pinterest.db'
CSV_FILE = 'pinterest_data.csv'

def initialize_database():
    """Create the database and posts table if it doesn't already exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            likes INTEGER,
            comments INTEGER,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_csv_data():
    """Load post data from a CSV file into the database."""
    if not os.path.exists(CSV_FILE):
        print(f"❌ CSV file '{CSV_FILE}' not found. Please make sure it's in the same folder.")
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    with open(CSV_FILE, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute('''
                INSERT INTO posts (title, author, likes, comments, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (row['title'], row['author'], int(row['likes']), int(row['comments']), row.get('category', '')))
    conn.commit()
    conn.close()
    print("✅ CSV data successfully imported into the database.")

def show_sample_data(limit=5):
    """Display a sample of posts from the database."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM posts LIMIT ?", (limit,))
    rows = c.fetchall()
    print("\n📌 Sample Posts:")
    for row in rows:
        print(row)
    conn.close()

def top_posts(metric='likes', limit=5):
    """List the top posts sorted by likes or comments."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    if metric not in ['likes', 'comments']:
        print("⚠️ Please choose a valid metric: 'likes' or 'comments'.")
        return
    c.execute(f'''
        SELECT title, author, {metric} FROM posts
        ORDER BY {metric} DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    print(f"\n🏆 Top {limit} Posts by {metric.capitalize()}:")
    for post in results:
        print(post)
    conn.close()

def plot_top_posts(metric='likes', limit=5):
    """Plot a bar chart of top posts by engagement metric."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(f'''
        SELECT title, {metric} FROM posts
        ORDER BY {metric} DESC
        LIMIT ?
    ''', (limit,))
    data = c.fetchall()
    titles = [row[0] for row in data]
    values = [row[1] for row in data]
    
    plt.barh(titles[::-1], values[::-1])
    plt.title(f"Top {limit} Posts by {metric.capitalize()}")
    plt.xlabel(metric.capitalize())
    plt.ylabel("Post Title")
    plt.tight_layout()
    plt.show()
    conn.close()

def main():
    """Main CLI loop for user interaction."""
    initialize_database()
    while True:
        print("\n📌 Pinterest CLI Menu")
        print("----------------------")
        print("1️⃣  Load data from CSV")
        print("2️⃣  Show sample data")
        print("3️⃣  View top posts by likes")
        print("4️⃣  View top posts by comments")
        print("5️⃣  Plot top posts by likes 📊")
        print("6️⃣  Plot top posts by comments 📊")
        print("0️⃣  Exit")

        choice = input("Select an option: ")
        if choice == '1':
            load_csv_data()
        elif choice == '2':
            show_sample_data()
        elif choice == '3':
            top_posts(metric='likes')
        elif choice == '4':
            top_posts(metric='comments')
        elif choice == '5':
            plot_top_posts(metric='likes')
        elif choice == '6':
            plot_top_posts(metric='comments')
        elif choice == '0':
            print("👋 Exiting Pinterest CLI. Have a great day!")
            break
        else:
            print("❌ Invalid option. Please choose from the menu.")

if __name__ == "__main__":
    main()
