import os
import anthropic
from dotenv import load_dotenv
import base64
import json

# Load environment variables from .env
load_dotenv()

# Initialize the Anthropic client
client = anthropic.Anthropic()

# Load test names from data.json
def load_test_names():
    with open('data/data.json') as f:
        data = json.load(f)
    return data['test_names']

# Function to extract blood data from an image
def extract_blood_data(image_path):
    test_name_list = load_test_names()  # Load test names from JSON
    prompt = f"""You are an AI assistant tasked with extracting blood test data from an image and formatting it as a CSV. Follow these instructions carefully:

1. You will be provided with an image of a blood test report

2. You will also be provided with a list of test names:
<test_name_list>
{test_name_list}
</test_name_list>

3. Analyze the image carefully, identifying all relevant information including test names, results, reference ranges, units, date of the test, and patient name.

4. Extract the following data for each test:
   - Test Name
   - Result
   - Reference Range
   - Units
   - Date
   - Patient's Name (split into Name and Surname)

5. Format the extracted data as a CSV with the following columns:
   'Test Name', 'Result', 'Reference Range', 'Units', 'Date', 'Name', 'Surname'

6. For the Date field, convert the date to the format 'YYYY-MM-DD'. If the year is not provided in the image, use the current year.

7. For the Name and Surname fields, split the patient's full name into two parts. If only one name is provided, put it in the 'Name' field and leave 'Surname' blank.

8. Only include tests that are present in the provided test_name_list. If a test name in the image doesn't exactly match any in the list but is very similar, use your judgment to include it with the closest matching name from the list.

9. If a test from the test_name_list is not found in the image, do not include it in the output.

10. Present your output as a CSV string, with each row on a new line and values separated by commas. Do not include quotation marks around the values unless they contain commas.

11. Do not include any explanations or additional text in your output, only the CSV data as specified.
    """

    # Open the image file and read it in binary mode
    with open(image_path, "rb") as image_file:
        image1_data = base64.b64encode(image_file.read()).decode("utf-8")

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image1_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
    )

    return response.content[0].text

# Function to process images, either from a directory or a single image path
def process_images(path):
    results = []  # Initialize a list to store results

    # Check if the path is a directory
    if os.path.isdir(path):
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                image_path = os.path.join(path, file)
                csv_file_path = os.path.join(path, f"{file[:-4]}.csv")  # CSV name without .jpg
                if os.path.exists(csv_file_path):  # Check if CSV already exists
                    print(f"File {csv_file_path} already exists, skipping.")
                    continue  # Skip to the next file if CSV exists
                result = extract_blood_data(image_path)  # Process the image
                results.append(result)  # Collect results
                # Save the result to a CSV file
                with open(csv_file_path, "w") as f:
                    f.write(result)
                print(f"File saved to {csv_file_path}")
    # If it's a single image file, process it directly
    elif os.path.isfile(path) and path.endswith(".jpg"):
        image_path = path
        csv_file_path = f"{image_path[:-4]}.csv"  # CSV name without .jpg
        if os.path.exists(csv_file_path):  # Check if CSV already exists
            print(f"File {csv_file_path} already exists, skipping.")
        else:
            result = extract_blood_data(image_path)  # Process the image
            results.append(result)  # Collect results
            # Save the result to a CSV file
            with open(csv_file_path, "w") as f:
                f.write(result)
            print(f"File saved to {csv_file_path}")
    else:
        print(f"Invalid path: {path}")

    return results  # Return the collected results

if __name__ == "__main__":
    # image_directory = "data/tamara_images"
    image_path = "data/tamara_cibrozzi/photo_5926902182848873542_y.jpg"
    process_images(image_path)
