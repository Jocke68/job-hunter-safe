import urllib.parse

def load_preferences():
    with open("preferences.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    print("=== Raw Preferences File ===")
    for line in lines:
        print("-", line)

    return lines


def split_preferences(lines):
    job_titles = []
    au_locations = []

    for line in lines:
        # Treat these as AU locations
        if any(keyword.lower() in line.lower() for keyword in ["sydney", "beaches", "nsw", "australia"]):
            au_locations.append(line)
        else:
            job_titles.append(line)

    print("\n=== Parsed Preferences ===")
    print("Job Titles:")
    for job in job_titles:
        print(" -", job)

    print("AU Locations:")
    for loc in au_locations:
        print(" -", loc)

    return job_titles, au_locations


def add_nz_locations():
    nz_locations = ["Christchurch", "Queenstown"]

    print("\nNZ Locations (added automatically):")
    for loc in nz_locations:
        print(" -", loc)

    return nz_locations


def build_indeed_urls(job_titles, au_locations, nz_locations):
    queries = []

    # AU searches
    for job in job_titles:
        for loc in au_locations:
            encoded_job = urllib.parse.quote_plus(job)
            encoded_loc = urllib.parse.quote_plus(loc)
            url = f"https://au.indeed.com/jobs?q={encoded_job}&l={encoded_loc}"
            queries.append({
                "country": "AU",
                "job_title": job,
                "location": loc,
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
    lines = load_preferences()
    job_titles, au_locations = split_preferences(lines)
    nz_locations = add_nz_locations()
    queries = build_indeed_urls(job_titles, au_locations, nz_locations)
    simulate_job_search(queries)
