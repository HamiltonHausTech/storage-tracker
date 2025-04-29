import json
import os
import shutil

DATA_FILE = 'bins.json'

# Load data
def load_bins():
    if not os.path.exists(DATA_FILE):
        return {"bins": []}
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Save data
def save_bins(data):
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, 'bins_backup.json')
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

# Add a new bin
def add_bin():
    data = load_bins()
    bin_name = input("Enter new bin name: ")
    bin_name = input("Enter new bin name: ").strip()
    if not bin_name:
        print("Bin name cannot be empty.")
        return

    location = input("Enter bin location: ")
    if not location:
        print("Location name cannot be empty")
        return
    
    data["bins"].append({"bin_name": bin_name, "location": location, "items": []})
    save_bins(data)
    print(f"Bin '{bin_name}' added successfully!")

# Add item to existing bin
def add_item_to_bin():
    data = load_bins()
    bin_name = input("Enter bin name to add item to: ")
    item = input("Enter item to add: ")
    for bin in data["bins"]:
        if bin["bin_name"].lower() == bin_name.lower():
            bin["items"].append(item)
            save_bins(data)
            print(f"Item '{item}' added to bin '{bin_name}'.")
            return
    choice = input(f"Bin '{bin_name}' not found. Create it? (y/n): ").lower()
    if choice == 'y':
        data["bins"].append({"bin_name": bin_name, "location": "Unknown", "items": [item]})
        save_bins(data)
        print(f"Created bin '{bin_name}' and added item '{item}'.")
    else:
        print("Item not added.")
        print(f"Bin '{bin_name}' not found.")

# Search for item
def search_items():
    data = load_bins()
    search_term = input("Enter item name to search: ").lower()
    found = False
    for bin in data["bins"]:
        for item in bin["items"]:
            if search_term in item.lower():
                print(f"Found '{item}' in {bin['bin_name']} (Location: {bin['location']})")
                found = True
    if not found:
        print("Item not found.")

# List all bins
def list_bins():
    data = load_bins()
    for bin in data["bins"]:
        print(f"{bin['bin_name']} - Location: {bin['location']}")
        if bin['items']:
            for item in bin['items']:
                print(f"  - {item}")

# Main menu
def main():
    while True:
        print("\nStorage Bin Tracker")
        print("1. Add New Bin")
        print("2. Add Item to Bin")
        print("3. Search for Item")
        print("4. List All Bins")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_bin()
        elif choice == '2':
            add_item_to_bin()
        elif choice == '3':
            search_items()
        elif choice == '4':
            list_bins()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
