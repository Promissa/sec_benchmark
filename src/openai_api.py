import base64
from openai import OpenAI
from src.html_parse import read_html

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "test/test_output/html_parse/10-K/brka-20241231/table_2.png"

# Getting the Base64 string
base64_image = encode_image(image_path)
raw = read_html("test/test_output/html_parse/10-K/brka-20241231/table_2.htm")

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": raw
                    + "\n\nParse the table in the given html file into markdown, duplicate any cells with span > 1",
                },
            ],
        }
    ],
)

print(response.output_text)
