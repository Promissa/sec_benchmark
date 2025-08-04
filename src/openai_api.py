import base64, tiktoken, cv2
from openai import OpenAI
from src.html_parse import read_html
from test.html_parse import gpt41_high_detail_token_cost

client = OpenAI()


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Path to your image
image_path = "test/test_output/10-K/brka-20241231/table_114.png"

# Getting the Base64 string
base64_image = encode_image(image_path)
raw = read_html("test/test_output/10-K/brka-20241231/table_114.htm")

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{base64_image}",
                    "detail": "high",
                },
                {
                    "type": "input_text",
                    "text": "Parse the table into markdown, duplicate any cells with span > 1. Only extract data that is visible when rendering and ignore any links if existing. Keep the indent using &nbsp;.",
                },
            ],
        }
    ],
)

print(response.output_text)
print(response.usage)
img = cv2.imread(image_path, 0)
print(gpt41_high_detail_token_cost(img.shape[1], img.shape[0]) + 44)
