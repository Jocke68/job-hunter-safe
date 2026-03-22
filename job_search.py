def load_preferences():
    with open("preferences.txt", "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    print("=== Raw Preferences File ===")
    for line in lines:
        print("-", line)

    return lines


def split_preferences(lines):
    job_titles = []
    locations = []

    for line in lines:
        # Simple rule:
        # If it contains words like "Sydney", "Beaches", "NSW", treat as location
        if any(keyword.lower() in line.lower() for keyword in ["sydney", "beaches", "nsw", "australia"]):
            locations.append(line)
        else:
            job_titles.append(line)

    print("\n=== Parsed Preferences ===")
    print("Job Titles:")
    for job in job_titles:
        print(" -", job)

    print("Locations:")
    for loc in locations:
        print(" -", loc)

    return job_titles, locations


def build_search_queries(job_titles, locations):
    queries = []

    for job in job_titles:
        for loc in locations:
            queries.append({
                "job_title": job,
                "location": loc,
                "query_string": f"{job} in {loc}"
            })

    print("\n=== Search Plan ===")
    for q in queries:
        print(f"- {q['query_string']}")

    return queries


def simulate_job_search(queries):
    print("\n=== Simulated Job Search ===")
    print("This is only a test — no real job sites are contacted.")

    for q in queries:
        print(f"\nSearching for: {q['query_string']}")
        print("Example result:")
        print(f"- {q['job_title']} role found in {q['location']} at ExampleCorp (simulated)")


if __name__ == "__main__":
    lines = load_preferences()
    job_titles, locations = split_preferences(lines)
    queries = build_search_queries(job_titles, locations)
    simulate_job_search(queries)
