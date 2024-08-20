# Web-Scraping
# web scrapping for Al Mayadeen Website
# Sitemap Article Scraper
This Python script is designed to scrape articles from a sitemap, extract key content and metadata, and save the articles into multiple JSON files, each containing up to 2,000 articles.

# Overview
The script fetches up to 10,000 article URLs from a sitemap, scrapes relevant content and metadata from each URL, and saves the data in JSON files in batches. This approach allows for efficient storage and easy management of large datasets.

# Key Features
Sitemap Parsing: Extracts article URLs directly from the sitemap.
Comprehensive Scraping: Captures essential metadata, including title, author, publication date, keywords, and the full text of the article.
Batch Processing: Saves the scraped articles into JSON files, with a maximum of 2,000 articles per file.
UTF-8 Support: Ensures that the output files handle special characters correctly.

# Prerequisites
Python 3.x
requests library
beautifulsoup4 library

# How to Use
Configure the Script:

Open the script and modify the following variables if needed:

URL_ALL: The sitemap URL to fetch the article links.
NUM_URLS: The total number of article URLs to process (default is 10,000).
ARTICLES_PER_FILE: The number of articles per JSON file (default is 2,000).

# Run the Script:

Execute the script to begin scraping:

python scrape_articles.py
The script will generate JSON files (e.g., articles_1.json, articles_2.json, etc.) in the working directory.

# Output
Each JSON file contains a list of articles, with each article's data stored as a dictionary including:
url: The original URL of the article.
post_id: A unique identifier for the article (if available).
title: The title of the article.
keywords: Keywords associated with the article.
thumbnail: URL to the article's thumbnail image.
publication_date: The article's publication date.
last_updated_date: The date the article was last updated.
author: The author of the article.
full_text: The full text of the article.
word_count: The total word count of the article.
language: The language of the article (default is English).
description: A brief description of the article.
class: The classification of the article (e.g., "news").

# Example Output
json

{
    "url": "https://example.com/article-1",
    "post_id": "123456",
    "title": "Sample Article Title",
    "keywords": ["news", "sample"],
    "thumbnail": "https://example.com/thumbnail.jpg",
    "publication_date": "2024-08-19T12:34:56Z",
    "last_updated_date": "2024-08-19T13:00:00Z",
    "author": "John Doe",
    "full_text": "This is the full text of the article.",
    "word_count": 350,
    "language": "en",
    "description": "Article scraped from https://example.com/article-1",
    "class": "news"
}

# Licens
This project is open-source and available under the MIT License.
