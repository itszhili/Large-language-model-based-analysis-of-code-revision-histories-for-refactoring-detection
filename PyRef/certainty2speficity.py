import json

def update_certainty_to_specificity(file_path):

    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    def replace_certainty(obj):
        if isinstance(obj, dict):
            new_obj = {}
            for key, value in obj.items():
                if key == 'Certainty':
                    new_obj['Specificity'] = replace_certainty(value)
                else:
                    new_obj[key] = replace_certainty(value)
            return new_obj
        elif isinstance(obj, list):
            return [replace_certainty(item) for item in obj]
        else:
            return obj

    updated_data = replace_certainty(data)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, indent=4, ensure_ascii=False)

file_path = 'face_recognition_data_with_classification.json'  
update_certainty_to_specificity(file_path)

print("JSON文件中的'certainty'字段已成功替换为'Specificity'")
