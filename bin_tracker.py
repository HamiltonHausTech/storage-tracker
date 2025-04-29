import json
import os
import shutil

from colorama import init, Fore, Style
init()
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
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "Bin name cannot be empty.")
        return

    location = input("Enter bin location: ")
    if not location:
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + "Location name cannot be empty")
        return
    
    data["bins"].append({"bin_name": bin_name, "location": location, "items": []})
    save_bins(data)
    print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + f"Bin '{bin_name}' added successfully!")

# Add item to existing bin
def add_item_to_bin():
    data = load_bins()
    bin_name = input("Enter bin name to add item to: ")
    item = input("Enter item to add: ")
    for bin in data["bins"]:
        if bin["bin_name"].lower() == bin_name.lower():
            bin["items"].append(item)
            save_bins(data)
            print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + f"Item '{item}' added to bin '{bin_name}'.")
            return
    choice = input(f"Bin '{bin_name}' not found. Create it? (y/n): ").lower()
    if choice == 'y':
        data["bins"].append({"bin_name": bin_name, "location": "Unknown", "items": [item]})
        save_bins(data)
        print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + f"Created bin '{bin_name}' and added item '{item}'.")
    else:
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + "Item not added.")
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + f"Bin '{bin_name}' not found.")

# Search for item
def search_items():
    data = load_bins()
    search_term = input("Enter item name to search: ").lower()
    found = False
    for bin in data["bins"]:
        for item in bin["items"]:
            if search_term in item.lower():
                print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + f"Found '{item}' in {bin['bin_name']} (Location: {bin['location']})")
                found = True
    if not found:
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + "Item not found.")

# List all bins
def list_bins():
    data = load_bins()
    for bin in data["bins"]:
        print("--------------------------------------")
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
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Source bin '{source_bin_name}' not found.")
        return
    if not target_bin:
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Target bin '{target_bin_name}' not found.")
        return

    # Try to find the item in the source bin
    item_found = None
    for item in source_bin["items"]:
        if item_name.lower() == item.lower():
            item_found = item
            break

    if not item_found:
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Item '{item_name}' not found in bin '{source_bin_name}'.")
        return

    # Move item
    confirm = input(f"Move '{item_found}' from '{source_bin_name}' to '{target_bin_name}'? (y/n): ").lower()
    if confirm == 'y':
        source_bin["items"].remove(item_found)
        target_bin["items"].append(item_found)
        save_bins(data)
        print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + f"Moved '{item_found}' from '{source_bin_name}' to '{target_bin_name}'.")
    else:
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + "[INFO] Move canceled.")

def remove_item_from_bin():
    data = load_bins()
    item_name = input("Enter the item you want to remove: ").strip()
    bin_name = input("Enter the bin name: ").strip()
    for bin in data["bins"]:
        if bin["bin_name"].lower() == bin_name.lower():
            source_bin = bin

    if not source_bin:
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Source bin '{bin_name}' not found.")
        return

    item_found = None
    for item in source_bin["items"]:
        if item_name.lower() == item.lower():
            item_found = item
            break

    if not item_found:
        print(Fore.RED + "[ERROR] " + Style.RESET_ALL + f"Item '{item_name}' not found in bin '{bin_name}'.")
        return

    confirm = input(f"Are you sure you want to remove '{item}' from bin '{bin_name}'? (y/n): ").lower()
    if confirm == 'y' or confirm == 'yes':
        source_bin["items"].remove(item)
        save_bins(data)
        print(Fore.GREEN + "[SUCCESS] " + Style.RESET_ALL + f"Item '{item}' removed from bin '{bin_name}'.")
    else:
        print(Fore.CYAN + "[INFO] " + Style.RESET_ALL + "[INFO] Removal canceled.")

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
            print(Fore.RED + "Invalid choice, try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()
