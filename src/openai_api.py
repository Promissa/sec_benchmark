import base64, tiktoken, cv2
from openai import OpenAI
from src.html_parse import read_html
from src.metrics import *
from test.html_parse import gpt41_high_detail_token_cost

client = OpenAI()
PROMPT = """
Parse the table into markdown. Duplicate the column header cells with colspan > 1 to keep the completeness of the structure.
Only extract data that is visible when rendering and ignore any links if existing.
Exclude all commas in numbers, e.g. "1,234" -> "1234". It's also required to keep bold and italic styles using markdown grammar 
Keep the indent using &nbsp; and separate signs as individual columns if possible. DO NOT CHANGE ANY TABLE CONTENT.
"""


def call_api(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
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
                        "text": PROMPT,
                    },
                ],
            }
        ],
    )

    # print(response.usage)
    img = cv2.imread(image_path, 0)
    # print(gpt41_high_detail_token_cost(img.shape[1], img.shape[0]) + 44)
    return response.output_text


if __name__ == "__main__":
    with open("result.md", "w") as f:
        f.write(
            call_api("test/test_output/10-K/brka-20241231/table_114.png")
            .strip()
            .strip("\n")
            .strip("```markdown")
            .strip("```")
        )
    print(
        cal_2d_lev(
            read_md("result.md"),
            read_md("test/test_output/10-K/brka-20241231/table_114.md"),
        )
    )
