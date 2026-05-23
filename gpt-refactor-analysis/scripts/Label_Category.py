import json

# Load JSON data from a file
def load_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Save JSON data to a file
def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def classify_refactoring(data, filename):
    sum = 0
    for item in data:
        # if 'Category2' in item:
        #     sum = sum +1
    # # Check if the item already has a Category key
        if "Category" in item:
            # Print current refactoring information
            print("\nCurrent refactoring information:")
            for key, value in item.items():
                print(f"{key}: {value}")

            # User input for classification
            print("Please classify this refactoring:\n 0: General\n 1: ML-Specific")
            choice = input("Enter your choice (0 or 1): ").strip()
            while choice not in ["0", "1"]:
                print("Invalid input, please enter 0 or 1.")
                choice = input("Enter your choice (0 or 1): ").strip()
                

            # Assign classification based on user input
            category = "General" if choice == "0" else "ML-Specific"
            
            # Add classification to the refactoring information, only adding a new key-value pair without changing the existing data structure
            item['Category2'] = category
            if "Category" in item:
                del item['Category']

            certainty = input("Enter the certainty from 0 to 5: ").strip()

            item['Certainty'] = certainty
            if "Uncertainty" in item:
                del item["Uncertainty"]
            
            # Save the data back to the JSON file after classifying each item
            save_json(filename, data)
            print('=' * 150)
    # print(sum)

 
# Filename
filename = 'DeepFaceLive_data_with_classification.json'
# Load data
refactorings_data = load_json(filename)

# Classify the refactoring data and save after each classification
classify_refactoring(refactorings_data, filename)

print("\nAll refactoring information has been classified and saved.")
