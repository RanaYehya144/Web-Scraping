import requests
from bs4 import BeautifulSoup as bs
import json
import sys

# Set default encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

URL_ALL = "https://www.almayadeen.net/sitemaps/all.xml"
NUM_URLS = 10000  # Number of URLs to process
ARTICLES_PER_FILE = 2000  # Number of articles per file


def fetch_xml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching the URL: {e}"


def extract_urls(xml_content):
    soup = bs(xml_content, 'xml')
    return [loc.text for loc in soup.find_all('loc')]


def get_sitemap_urls():
    xml_content = fetch_xml(URL_ALL)
    if not xml_content.startswith("Error"):
        urls = extract_urls(xml_content)
        return urls[:NUM_URLS] if len(urls) > NUM_URLS else urls
    else:
        return xml_content


def gather_article_links():
    sitemap_urls = get_sitemap_urls()
    if not isinstance(sitemap_urls, list):
        return sitemap_urls  # return the error message if any

    article_urls = []
    for sitemap_url in sitemap_urls:
        xml_content = fetch_xml(sitemap_url)
        if not xml_content.startswith("Error"):
            article_urls.extend(extract_urls(xml_content))
    return article_urls


def scrape_article_content(url):
    html_content = fetch_xml(url)
    if html_content.startswith("Error"):
        return html_content

    soup = bs(html_content, 'html.parser')

    article_data = {
        "url": url,
        "video_duration": 0,  # Always 0 as requested
    }

    post_id_meta = soup.find('meta', {'name': 'postid'})
    article_data["post_id"] = post_id_meta['content'] if post_id_meta else 'No post ID found'

    details_white_box = soup.find('div', class_='details-white-box')
    article_data["title"] = details_white_box.find('h2').text if details_white_box and details_white_box.find(
        'h2') else 'No title found'

    keywords_meta = soup.find('meta', {'name': 'keywords'})
    article_data["keywords"] = keywords_meta['content'].split(',') if keywords_meta else 'No keywords found'

    thumbnail_meta = soup.find('meta', {'property': 'og:image'})
    article_data["thumbnail"] = thumbnail_meta['content'] if thumbnail_meta else 'No thumbnail found'

    pub_date_meta = soup.find('meta', {'property': 'article:published_time'})
    article_data["publication_date"] = pub_date_meta['content'] if pub_date_meta else 'No publication date found'

    last_updated_meta = soup.find('meta', {'property': 'article:modified_time'})
    article_data["last_updated_date"] = last_updated_meta['content'] if last_updated_meta else 'No last updated date found'

    author_meta = soup.find('meta', {'name': 'author'})
    article_data["author"] = author_meta['content'] if author_meta else 'No author found'

    paragraphs = soup.find_all('p')
    full_text = "\n".join([para.text for para in paragraphs])
    article_data["full_text"] = full_text

    # Additional metadata
    article_data["word_count"] = len(full_text.split())
    article_data["language"] = "en"  # Assuming English language; adjust as needed
    article_data["description"] = f"Article scraped from {url}"
    article_data["class"] = "news"  # Example class; adjust as needed

    return article_data


def save_articles_to_json(articles, file_index):
    filename = f'articles_{file_index}.json'
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(articles)} articles to {filename}")


# Main script execution
if __name__ == "__main__":
    article_urls = gather_article_links()
    if isinstance(article_urls, list):
        all_articles = []
        file_index = 1

        for i, url in enumerate(article_urls[:NUM_URLS]):
            article_data = scrape_article_content(url)
            all_articles.append(article_data)

            # Save articles in batches of ARTICLES_PER_FILE
            if (i + 1) % ARTICLES_PER_FILE == 0 or (i + 1) == len(article_urls[:NUM_URLS]):
                save_articles_to_json(all_articles, file_index)
                all_articles = []  # Reset list for the next batch
                file_index += 1
    else:
        print(article_urls)
