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

def move_item_to_bin():
    data = load_bins()

    item_name = input("Enter the item you want to move: ").strip()
    source_bin_name = input("Enter the current bin name: ").strip()
    target_bin_name = input("Enter the target bin name: ").strip()

    source_bin = None
    target_bin = None

    for bin in data["bins"]:
        if bin["bin_name"].lower() == source_bin_name.lower():
            source_bin = bin
        if bin["bin_name"].lower() == target_bin_name.lower():
            target_bin = bin

    if not source_bin:
        print(f"[ERROR] Source bin '{source_bin_name}' not found.")
        return
    if not target_bin:
        print(f"[ERROR] Target bin '{target_bin_name}' not found.")
        return

    # Try to find the item in the source bin
    item_found = None
    for item in source_bin["items"]:
        if item_name.lower() == item.lower():
            item_found = item
            break

    if not item_found:
        print(f"[ERROR] Item '{item_name}' not found in bin '{source_bin_name}'.")
        return

    # Move item
    source_bin["items"].remove(item_found)
    target_bin["items"].append(item_found)
    save_bins(data)
    print(f"[SUCCESS] Moved '{item_found}' from '{source_bin_name}' to '{target_bin_name}'.")

def remove_item_from_bin():
    data = load_bins()
    item_name = input("Enter the item you want to remove: ").strip()
    bin_name = input("Enter the bin name: ").strip()
    for bin in data["bins"]:
        if bin["bin_name"].lower() == bin_name.lower():
            source_bin = bin

    if not source_bin:
        print(f"[ERROR] Source bin '{bin_name}' not found.")
        return

    item_found = None
    for item in source_bin["items"]:
        if item_name.lower() == item.lower():
            item_found = item
            break

    if not item_found:
        print(f"[ERROR] Item '{item_name}' not found in bin '{bin_name}'.")
        return

    source_bin["items"].remove(item_found)
    save_bins(data)
    print(f"[SUCCESS] Removed '{item_found}' from '{bin_name}'.")




# Main menu
def main():
    while True:
        print("\nStorage Bin Tracker")
        print("1. Add New Bin")
        print("2. Add Item to Bin")
        print("3. Remove Item from Bin")
        print("4. Search for Item")
        print("5. Move Item to another bin")
        print("6. List All Bins")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_bin()
        elif choice == '2':
            add_item_to_bin()
        elif choice == '3':
            remove_item_from_bin()
        elif choice == '4':
            search_items()
        elif choice == '5':
            move_item_to_bin()
        elif choice == '6':
            list_bins()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
