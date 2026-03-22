import yaml
import urllib.parse

def load_preferences():
    with open("preferences.txt", "r") as f:
        data = yaml.safe_load(f)

    print("=== Loaded YAML Preferences ===")
    print(data)

    return data


def extract_preferences(data):
    # Extract job titles
    job_titles = data.get("job_titles", [])
    # Flatten nested lists if needed
    job_titles = [item for sublist in job_titles for item in (sublist if isinstance(sublist, list) else [sublist])]

    # Extract AU location
    au_location = data.get("location", "Sydney, Australia")

    print("\n=== Parsed Preferences ===")
    print("Job Titles:")
    for job in job_titles:
        print(" -", job)

    print("AU Location:")
    print(" -", au_location)

    return job_titles, au_location


def add_nz_locations():
    nz_locations = ["Christchurch", "Queenstown"]

    print("\nNZ Locations (added automatically):")
    for loc in nz_locations:
        print(" -", loc)

    return nz_locations


def build_indeed_urls(job_titles, au_location, nz_locations):
    queries = []

    # AU searches
    for job in job_titles:
        encoded_job = urllib.parse.quote_plus(job)
        encoded_loc = urllib.parse.quote_plus(au_location)
        url = f"https://au.indeed.com/jobs?q={encoded_job}&l={encoded_loc}"
        queries.append({
            "country": "AU",
            "job_title": job,
            "location": au_location,
            "url": url
        })

    # NZ searches
    for job in job_titles:
        for loc in nz_locations:
            encoded_job = urllib.parse.quote_plus(job)
            encoded_loc = urllib.parse.quote_plus(loc)
            url = f"https://nz.indeed.com/jobs?q={encoded_job}&l={encoded_loc}"
            queries.append({
                "country": "NZ",
                "job_title": job,
                "location": loc,
                "url": url
            })

    print("\n=== Indeed Search URLs ===")
    for q in queries:
        print(f"[{q['country']}] {q['job_title']} in {q['location']}")
        print(" ", q["url"])

    return queries


def simulate_job_search(queries):
    print("\n=== Simulated Job Search ===")
    print("This is only a test — no real job sites are contacted.")

    for q in queries:
        print(f"\nSearching: {q['job_title']} in {q['location']} ({q['country']})")
        print("Example result:")
        print(f"- {q['job_title']} role found in {q['location']} at ExampleCorp (simulated)")


if __name__ == "__main__":
    data = load_preferences()
    job_titles, au_location = extract_preferences(data)
    nz_locations = add_nz_locations()
    queries = build_indeed_urls(job_titles, au_location, nz_locations)
    simulate_job_search(queries)
