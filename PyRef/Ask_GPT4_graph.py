import openai
import json
import os
import textwrap
import fire
import logging
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Load API key from environment variable (recommended approach)
# openai_api_key = os.getenv("OPENAI_API_KEY")

# Create an OpenAI client
load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Path to JSON file
json_file_path = '/mimer/NOBACKUP/groups/2023-llm-refactoring/PyRef/face_recognition_data.json'
output_json_suffix = '_GPT4_graph_new.json'

# Generate the output file name
base_name = os.path.basename(json_file_path)
name_without_ext = os.path.splitext(base_name)[0]
output_file_name = name_without_ext + output_json_suffix
output_file_path = os.path.join(os.path.dirname(json_file_path), output_file_name)

# Load JSON data
with open(json_file_path, 'r') as file:
    refactoring_data = json.load(file)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def format_classification_text(text, width=100):
    """
    Splits the classification text into a list of strings at a specified width.
    
    Args:
        text (str): The text to format.
        width (int): The desired width before breaking into a new list item.
        
    Returns:
        List[str]: The formatted text as a list of lines.
    """
    return textwrap.wrap(text, width)

def classify_with_gpt(content, custom_question=None, model="gpt-4", temperature=0.6, max_tokens=10):
    """
    Classify the refactoring using GPT chat model.

    Args:
        content (str): The content describing the refactoring to be classified.
        custom_question (str, optional): A custom question for the classification. Defaults to None.
        model (str, optional): The GPT model to use. Defaults to "gpt-4".
        temperature (float, optional): Sampling temperature. Defaults to 0.6.
        max_tokens (int, optional): Maximum tokens to generate. Defaults to 10.

    Returns:
        str: The GPT classification result (either "general" or "machine-learning-specific").
    """
    try:
        # If a custom question is provided, use it; otherwise, use the default question
        if custom_question:
            question = custom_question
        else:
            # question = f"""{content} 
            # Classify this refactoring into one of these categories: DATA_PIPELINE, MODEL_LOGIC, TRAINING_PROCESS, EVALUATION_MONITORING, or DEPLOYMENT_INFRASTRUCTURE. 
            # Answer with only the category name."""
            question = f"""{content} 
            Classify this refactoring into one of these categories: Data Processing, Model Development, Evaluation, Deployment & Serving, Visualization & UI, or Monitoring & Logging. 
            Answer with only the category name."""
        
        # Log the question before making the request
        logger.info(f"Question for GPT: {question}")

        # Use the client to make a chat completion request
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": question
                },
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        answer = completion.choices[0].message.content.strip()
        return answer
    except Exception as e:
        logger.error(f"API call failed: {e}")
        return None

def filter_content(block, included_fields=None):
    """
    Filter content based on included fields from a block to construct content for GPT classification.

    Args:
        block (dict): A single block of the JSON data representing a refactoring.
        included_fields (list): List of keys to include in the content.

    Returns:
        str: The filtered content as a string, including only specified fields.
    """
    if included_fields is None:
        included_fields = ["Description", "Location"]

    # Create a list of key-value pairs, including only desired fields
    key_value_pairs = [
        f"{key}: {block[key]}" for key in included_fields if key in block
    ]
    
    return ", ".join(key_value_pairs)

def main(model: str = "gpt-4", temperature: float = 0, max_tokens: int = 10, included_fields=None):
    """
    Main function to classify refactorings and append classifications to JSON.

    Args:
        model (str, optional): The GPT model to use. Defaults to "gpt-4".
        temperature (float, optional): Sampling temperature for GPT. Defaults to 0.6.
        max_tokens (int, optional): Maximum tokens for GPT output. Defaults to 10.
        excluded_fields (list, optional): List of fields to exclude from the classification content.
    """
    if included_fields is None:
        included_fields=["Description", "Location"]

    for idx, block in enumerate(refactoring_data):
        # Filter content, excluding certain fields
        content = filter_content(block, included_fields=included_fields)


        # For the first block, use the custom question
        # if idx == 0:
        # custom_question = f"""
        # 1."Description" "The parameters [ model ] are added to the method face_encodings from the module face_recognition/api.py"
        # "Patch Information" "@@ -200,16 +200,17 @@ def face_landmarks(face_image, face_locations=None, model=\"large\"):\n         raise ValueError(\"Invalid landmarks model type. Supported models are ['small', 'large'].\")\n \n \n-def face_encodings(face_image, known_face_locations=None, num_jitters=1):\n+def face_encodings(face_image, known_face_locations=None, num_jitters=1, model=\"small\"):\n     \"\"\"\n     Given an image, return the 128-dimension face encoding for each face in the image.\n \n     :param face_image: The image that contains one or more faces\n     :param known_face_locations: Optional - the bounding boxes of each face if you already know them.\n     :param num_jitters: How many times to re-sample the face when calculating encoding. Higher is more accurate, but slower (i.e. 100 is 100x slower)\n+    :param model: Optional - which model to use. \"large\" (default) or \"small\" which only returns 5 points but is faster.\n     :return: A list of 128-dimensional face encodings (one for each face in the image)\n     \"\"\"\n-    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model=\"small\")\n+    raw_landmarks = _raw_face_landmarks(face_image, known_face_locations, model)\n     return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]\n \n \ndiff --git a/tests/test_face_recognition.py b/tests/test_face_recognition.py\nindex c0e550057..8eee9bb02 100644\n--- a/tests/test_face_recognition.py\n+++ b/tests/test_face_recognition.py\n"
        # "Category": "ML-Specific"
        # 2."Description" "The method css_to_rect from the module face_recognition/api.py is renamed to _css_to_rect"
        # "Patch Information""@@ -12,28 +12,31 @@\n face_encoder = dlib.face_recognition_model_v1(face_recognition_model)\n \n \n-def rect_to_css(rect):\n+def _rect_to_css(rect):\n     \"\"\"\n     Convert a dlib 'rect' object to a plain tuple in (top, right, bottom, left) order\n+\n     :param rect: a dlib 'rect' object\n     :return: a plain tuple representation of the rect in (top, right, bottom, left) order\n     \"\"\"\n     return rect.top(), rect.right(), rect.bottom(), rect.left()\n \n \n-def css_to_rect(css):\n+def _css_to_rect(css):\n     \"\"\"\n     Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object\n+\n     :param css:  plain tuple representation of the rect in (top, right, bottom, left) order\n     :return: a dlib `rect` object\n     \"\"\"\n     return dlib.rectangle(css[3], css[0], css[1], css[2])\n \n \n-def face_distance(faces, face_to_compare):\n+def _face_distance(faces, face_to_compare):\n     \"\"\"\n     Given a list of face encodings, compared them to a known face encoding and get a euclidean distance\n     for each comparison face.\n+\n     :param faces: List of face encodings to compare\n     :param face_to_compare: A face encoding to compare against\n     :return: A list with the distance for each face in the same order as the 'faces' array\n"
        # "Category2": "General"

        # Classify the following refactorings as either machine-learning-specific or general. Answer with only one word: general or machine-learning-specific. {content}"""
        
        # 3."The parameters [ freeze_z_rotation ] are added to the method cut from the module xlib/face/FLandmarks2D.py in class FLandmarks2D"
        # "Category2": "ML-Specific","Specificity": "3"

        # 4."The method get_name from the module xlib/console/diacon/Diacon.py in class DlgChoice is renamed to get_short_name"
        # "Category2": "General","Specificity": "4"        
        # custom_question = f"""
        # Classify the following refactorings as either machine-learning-specific or general. Answer with only one word: general or machine-learning-specific. {content}"""
        classification = classify_with_gpt(content, model=model, temperature=temperature, max_tokens=max_tokens)
        # else:
        #     # For other blocks, use the default classification process
        #     classification = classify_with_gpt(content, model=model, temperature=temperature, max_tokens=max_tokens)

        if classification:
            block['Component GPT4 New'] = classification
        else:
            block['Component GPT4 New'] = ["Failed to classify"]


    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(refactoring_data, file, ensure_ascii=False, indent=4)

    print(f"Classifications saved to {output_file_path}")

if __name__ == "__main__":
    fire.Fire(main)
