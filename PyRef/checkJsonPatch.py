import json

def check_patch_information(json_file_path):
    with open(json_file_path, "r") as file:
        data = json.load(file)

    print("Checking each entry for 'Patch Information'...")

    valid_count = 0  # Counter for valid entries
    invalid_count = 0  # Counter for invalid entries

    for entry in data:
        patch_info = entry.get("Patch Information", [])

        # Check if 'Patch Information' contains exactly one entry
        if isinstance(patch_info, list) and len(patch_info) == 1:
            valid_count += 1
        else:
            invalid_count += 1
            print("\nEntry with incorrect 'Patch Information':")
            print(json.dumps(entry, indent=4))

    # Print success and failure summary
    print(f"\nCheck completed! {valid_count} entries passed, {invalid_count} entries didn't pass.")

if __name__ == "__main__":
    json_file_path = "DeepFaceLive_data2.json"  # Replace with your JSON file path
    check_patch_information(json_file_path)
