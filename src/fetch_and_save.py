import os
import re
from newsapi import NewsApiClient
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import time
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)

def sanitize_text(text):
    # Use BeautifulSoup to remove any HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

def scrape_article_content(url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # This is a basic scraper and may need to be adjusted for different websites
        paragraphs = soup.find_all('p')
        content = ' '.join([p.text for p in paragraphs])
        
        return content
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return "Scraping failed"

def create_pdf(title, description, content, published_at, author, source_name, url, file_path):
    doc = SimpleDocTemplate(file_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=4))  # 4 is for justified text
    
    story = []
    
    # Sanitize all text inputs
    title = sanitize_text(title)
    description = sanitize_text(description)
    content = sanitize_text(content)
    author = sanitize_text(author)
    source_name = sanitize_text(source_name)
    
    # Title
    story.append(Paragraph(title, styles['Title']))
    story.append(Spacer(1, 12))
    
    # Metadata
    story.append(Paragraph(f"Author: {author}", styles['Italic']))
    story.append(Paragraph(f"Source: {source_name}", styles['Italic']))
    story.append(Paragraph(f"Published: {published_at}", styles['Italic']))
    story.append(Paragraph(f"URL: {url}", styles['Italic']))
    story.append(Spacer(1, 12))
    
    # Description
    story.append(Paragraph("Description:", styles['Heading2']))
    story.append(Paragraph(description, styles['Justify']))
    story.append(Spacer(1, 12))
    
    # Content
    story.append(Paragraph("Full Content:", styles['Heading2']))
    story.append(Paragraph(content, styles['Justify']))
    
    doc.build(story)

def NewsFromTopic(newsapi, topic):
    to_date = datetime.now().strftime('%Y-%m-%d')
    from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

    all_articles = newsapi.get_everything(q=topic,
                                          from_param=from_date,
                                          to=to_date,
                                          language='en',
                                          sort_by='publishedAt',
                                          page_size=50)

    dir_path = os.path.join(os.getcwd(), "downloads", topic)
    os.makedirs(dir_path, exist_ok=True)

    for article in all_articles['articles']:
        try:
            title = article.get("title", "No Title")
            description = article.get("description", "No Description")
            published_at = article.get("publishedAt", "No Date")
            author = article.get("author", "No Author")
            source_name = article.get("source", {}).get("name", "No Source")
            url = article.get("url", "No URL")

            # Scrape full content
            full_content = scrape_article_content(url)

            filename = sanitize_filename(title) + ".pdf"
            file_path = os.path.join(dir_path, filename)

            create_pdf(title, description, full_content, published_at, author, source_name, url, file_path)

            print(f"Article '{title}' saved to {file_path}")
        except Exception as e:
            print(f"Error processing article: {str(e)}")
        
        # Be polite and don't hammer the servers
        time.sleep(1)

# Driver code
if __name__ == '__main__':
    API_KEY = "4551a6273a4d4c108e84433db9b7f9f5"
    newsapi = NewsApiClient(api_key=API_KEY)
    
    topics = ["Economy", "Politics", "Sports", "Technology", "Business", "Entertainment", "Science", "Health"]
    
    for topic in topics:
        NewsFromTopic(newsapi, topic)