import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import random

# Define chunking parameters
CHUNK_SIZE = 200
OVERLAP = 50

# List of URLs
URLS = [
    "https://www.reddit.com/r/UCI/",
    "https://www.reddit.com/r/UCI/comments/1jckpkn/first_year_housing_scoop/",
    "https://www.reddit.com/r/UCI/comments/1jh388v/current_incoming_2029_students_faq_megathread/",
    "https://www.reddit.com/r/UCI/comments/w1ooph/how_to_request_assistance_in_a_time_of_crisis/",
    "https://www.reddit.com/r/UCI/comments/vfp0la/uci_housing_megathread_20222023/",
    "https://www.admissions.uci.edu/study/majors-minors.php?type=Major",
    "https://www.reddit.com/r/UCI/comments/1d25n2j/",
    "https://www.reddit.com/r/UCI/comments/1d25n2j/comp_sci_majors_are_you_struggling_to_find_a_job/",
    "https://www.reddit.com/r/UCI/comments/194da57/why_are_cs_majors_so_gross/",
    "https://www.reddit.com/r/UCI/comments/1t57ayb/tips_for_prospective_undergraduate_cs_majors_at/",
    "https://www.reddit.com/r/UCI/comments/1sy66rb/uci_international_students_fall_2026_winter_2027/",
    "https://www.reddit.com/r/UCI/comments/1fo190s/can_you_name_5_good_or_bad_things_you_experienced/",
    "https://www.reddit.com/r/UCI/comments/1bm7u59/prosconsthoughts_from_currentrecent_undergrads/",
    "https://www.roomsurf.com/dorm-reviews/uci/middle-earth-towers/15309",
   "https://housing.uci.edu/first-year/",
   "https://housing.uci.edu/middle-earth/",
   "https://housing.uci.edu/mesa-court/"


]

def scrape_url(url):
    """Scrape content from a URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Extract main content (customize based on the website structure)
        if "reddit.com" in url:
            # For Reddit, extract post content
            content = soup.find_all("div", {"data-test-id": "post-content"})
            return " ".join([c.get_text() for c in content])
        else:
            # For other websites, extract all text
            return soup.get_text()
    else:
        print(f"Failed to scrape {url} (Status code: {response.status_code})")
        return ""

def clean_text(text):
    """Clean raw text by removing unwanted content."""
    # Remove HTML entities and extra whitespace
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def chunk_text(text, chunk_size, overlap):
    """Split text into chunks with overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def save_chunks(chunks, output_dir, file_name):
    """Save chunks to a file."""
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{file_name}_chunks.txt")
    with open(output_path, "w", encoding="utf-8") as file:
        for i, chunk in enumerate(chunks):
            file.write(f"Chunk {i + 1}:\n{chunk}\n\n")

def main():
    output_dir = "processed_chunks"

    for i, url in enumerate(URLS):
        print(f"Scraping URL {i + 1}/{len(URLS)}: {url}")
        raw_text = scrape_url(url)
        if raw_text:
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text, CHUNK_SIZE, OVERLAP)
            save_chunks(chunks, output_dir, f"document_{i + 1}")
            print(f"Processed {len(chunks)} chunks for URL {i + 1}")

# def main():
#     # Define output directory
#     output_dir = "processed_chunks"

#     # Count number of chunks
#     total_chunks = 0
#     # Process each URL
#     for i, url in enumerate(URLS):
#         print(f"Scraping URL {i + 1}/{len(URLS)}: {url}")
#         raw_text = scrape_url(url)
#         if raw_text:
#             cleaned_text = clean_text(raw_text)
#             chunks = chunk_text(cleaned_text, CHUNK_SIZE, OVERLAP)
#             save_chunks(chunks, output_dir, f"url_{i + 1}")

#             # Increment chunk counter
#             total_chunks += len(chunks)

#             # Print 5 random chunks for verification
#             print(f"\n--- Verifying chunks for URL {i + 1} ---")
#             if len(chunks) > 5:
#                 random_chunks = random.sample(chunks, 5)
#             else:
#                 random_chunks = chunks  # If fewer than 5 chunks, print all
#             for j, chunk in enumerate(random_chunks):
#                 print(f"Random Chunk {j + 1}:\n{chunk}\n")

#     print(f"\nTotal number of chunks processed: {total_chunks}")

# if __name__ == "__main__":
#     main()