import yaml
import urllib.parse
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------
# Load YAML preferences
# ---------------------------------------------------------
def load_preferences():
    with open("preferences.txt", "r") as f:
        data = yaml.safe_load(f)

    print("=== Loaded YAML Preferences ===")
    print(data)

    return data


# ---------------------------------------------------------
# Extract job titles + AU location
# ---------------------------------------------------------
def extract_preferences(data):
    job_titles = data.get("job_titles", [])
    job_titles = [
        item for sublist in job_titles
        for item in (sublist if isinstance(sublist, list) else [sublist])
    ]

    au_location = data.get("location", "Sydney, Australia")

    print("\n=== Parsed Preferences ===")
    print("Job Titles:")
    for job in job_titles:
        print(" -", job)

    print("AU Location:")
    print(" -", au_location)

    return job_titles, au_location


# ---------------------------------------------------------
# Add NZ locations automatically
# ---------------------------------------------------------
def add_nz_locations():
    nz_locations = ["Christchurch", "Queenstown"]

    print("\nNZ Locations (added automatically):")
    for loc in nz_locations:
        print(" -", loc)

    return nz_locations


# ---------------------------------------------------------
# Build Indeed URLs for AU + NZ
# ---------------------------------------------------------
def build_indeed_urls(job_titles, au_location, nz_locations):
    queries = []

    # AU searches
    for job in job_titles:
        encoded_job = urllib.parse.quote_plus(job)
        encoded_loc = urllib.parse.quote_plus(au_location)
        url = f"https://au.indeed.com/jobs?q={encoded_job}&l={encoded_loc}"
        queries.append(("AU", job, au_location, url))

    # NZ searches
    for job in job_titles:
        for loc in nz_locations:
            encoded_job = urllib.parse.quote_plus(job)
            encoded_loc = urllib.parse.quote_plus(loc)
            url = f"https://nz.indeed.com/jobs?q={encoded_job}&l={encoded_loc}"
            queries.append(("NZ", job, loc, url))

    print("\n=== Indeed Search URLs ===")
    for country, job, loc, url in queries:
        print(f"[{country}] {job} in {loc}")
        print(" ", url)

    return queries


# ---------------------------------------------------------
# Aggressive scraper + DEBUG HTML
# ---------------------------------------------------------
def fetch_indeed_results(url, max_results=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    html = response.text

    # DEBUG: print first 500 chars of HTML
    print("\n--- DEBUG HTML START ---")
    print(html[:500])
    print("--- DEBUG HTML END ---\n")

    soup = BeautifulSoup(html, "html.parser")

    results = []

    # Try multiple selectors (aggressive mode)
    selectors = [
        "a.tapItem",
        "div.job_seen_beacon",
        "td.resultContent",
        "div.slider_container",
        "h2.jobTitle span"
    ]

    for selector in selectors:
        cards = soup.select(selector)
        for card in cards:
            title = card.select_one("h2.jobTitle span")
            company = card.select_one("span.companyName")

            # Determine link
            link = None
            if card.name == "a":
                link = card.get("href")
            else:
                parent = card.find_parent("a")
                if parent:
                    link = parent.get("href")

            if title and company and link:
                results.append((title.text.strip(), company.text.strip(), "https://indeed.com" + link))
                if len(results) >= max_results:
                    return results

    return results


# ---------------------------------------------------------
# Run real job search
# ---------------------------------------------------------
def run_real_job_search(queries):
    print("\n=== REAL JOB SEARCH RESULTS ===")

    for country, job, loc, url in queries:
        print(f"\nSearching for: {job} in {loc} ({country})")
        print("URL:", url)

        results = fetch_indeed_results(url, max_results=5)

        if not results:
            print("No results found.")
            continue

        for title, company, link in results:
            print(f"- {title} at {company}")
            print(f"  {link}")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
if __name__ == "__main__":
    data = load_preferences()
    job_titles, au_location = extract_preferences(data)
    nz_locations = add_nz_locations()
    queries = build_indeed_urls(job_titles, au_location, nz_locations)
    run_real_job_search(queries)
