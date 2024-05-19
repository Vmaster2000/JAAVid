import os
from google.cloud import vision
import io

# Set up Google Cloud Vision client
def setup_vision_client():
    # Ensure the environment variable is set to your service account key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"
    client = vision.ImageAnnotatorClient()
    return client

def extract_text_from_image(image_path, client):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if response.error.message:
        raise Exception(f"{response.error.message}")

    if texts:
        extracted_text = texts[0].description
    else:
        extracted_text = ""

    return extracted_text

def main():
    # Set the path to your service account key file if not already set
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path_to_your_service_account_key.json"

    # Initialize the Vision API client
    client = setup_vision_client()

    # Path to the image you want to process
    image_path = 'path_to_your_image.jpg'

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path, client)

    # Print the extracted text
    print("Extracted Text:")
    print(extracted_text)

if __name__ == "__main__":
    main()
