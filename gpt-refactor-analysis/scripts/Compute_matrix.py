import json

def normalize_string(s):
    # Normalize the string by stripping whitespace, converting to lower case, and replacing certain characters
    return s.strip().lower().replace('-', ' ').replace('_', ' ')

def main():
    filename1 = 'face_recognition_data_few_shot_with_gpt_classification.json' # GPT 4 classification
    filename2 = 'face_recognition_data_with_classification.json'  # Ground Truth

    # Initialize counts
    TN = 0  # True Non-ML-Specific
    FN = 0  # False Negative
    TP = 0  # True Positive
    FP = 0  # False Positive
    Unmatched = 0  # Count of unmatched items

    # Read the JSON files
    with open(filename1, 'r', encoding='utf-8') as f1:
        data1 = json.load(f1)

    with open(filename2, 'r', encoding='utf-8') as f2:
        data2 = json.load(f2)

    # Check that both files have the same number of items
    if len(data1) != len(data2):
        print("Error: The two JSON files do not have the same number of items.")
        return

    # Total number of items in data1 (or data2, since they are expected to be the same length)
    total_items = len(data1)

    # Iterate over both JSON data sets in parallel
    for idx, (item1, item2) in enumerate(zip(data1, data2)):
        # Extract 'GPT4 Classification' from the first file and 'Category2' from the second file
        gpt4_classification = item1.get("GPT4 Classification", [])
        category2 = item2.get("Category2", "")

        gpt4_classification_value = item1.get("GPT4 Classification", "")    

        # Normalize the strings for comparison
        gpt4_classification_value_norm = normalize_string(gpt4_classification_value)
        category2_norm = normalize_string(category2)

        # Compare and update counts
        if gpt4_classification_value_norm == "general" and category2_norm == "general":
            TN += 1
        elif gpt4_classification_value_norm == "general" and category2_norm == "ml specific":
            FN += 1
        elif gpt4_classification_value_norm == "machine learning specific" and category2_norm == "ml specific":
            TP += 1
        elif gpt4_classification_value_norm == "machine learning specific" and category2_norm == "general":
            FP += 1
        else:
            Unmatched += 1
            # Print unmatched cases for debugging
            print(f"Unmatched case at index {idx}:")
            print(f"  GPT4 Classification: '{gpt4_classification_value}' (normalized: '{gpt4_classification_value_norm}')")
            print(f"  Category2: '{category2}' (normalized: '{category2_norm}')\n")

    # Calculate Total, Precision, Recall, and F1 score
    Total = TN + FN + TP + FP
    Precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    Recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    F1_score = 2 * Precision * Recall / (Precision + Recall) if (Precision + Recall) > 0 else 0

    # Print the results
    print(f"Total Items in Data: {total_items}")
    print(f"Total Counted Items (TN + FN + TP + FP): {Total}")
    print(f"Unmatched Items: {Unmatched}\n")

    print(f"True Positive (TP): {TP}")
    print(f"False Positive (FP): {FP}")
    print(f"True Non-ML-Specific (TN): {TN}")
    print(f"False Negative (FN): {FN}\n")

    print(f"Precision: {Precision:.4f}")
    print(f"Recall: {Recall:.4f}")
    print(f"F1 score: {F1_score:.4f}")

if __name__ == "__main__":
    main()
