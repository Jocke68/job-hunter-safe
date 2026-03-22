import yaml

def load_preferences():
    with open("preferences.txt", "r") as f:
        content = f.read()
    print("=== Preferences File ===")
    print(content)
    return content

def simulate_job_search(preferences_text):
    print("\n=== Simulated Job Search ===")
    print("Pretending to search for jobs based on your preferences...")
    print("This is only a test — no real job sites are contacted.")
    print("\nExample result:")
    print("- Warehouse Supervisor role found at ExampleCorp (simulated)")

if __name__ == "__main__":
    prefs = load_preferences()
    simulate_job_search(prefs)
