import yaml

def load_preferences():
    with open("preferences.txt", "r") as f:
        content = f.read()
    print("=== Preferences File ===")
    print(content)

if __name__ == "__main__":
    load_preferences()
