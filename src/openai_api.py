import base64, tiktoken, cv2
from openai import OpenAI
from src.html_parse import read_html
from src.metrics import *
from test.html_parse import gpt41_high_detail_token_cost

client = OpenAI()
INSTRUCTION = """
Extract the complete table structure from the given image into Markdown format without any extra content, following the requirements below.

### Requirements:
1. **Preserve structure**: Duplicate column headers with `colspan > 1` to maintain structural completeness.
2. **Visible content only**: Extract only what is visible in the rendered image; ignore hyperlinks.
3. **Normalize numbers**: Remove commas from numbers (e.g., `1,234` → `1234`).
4. **Markdown formatting**: Retain **bold** and *italic* styles using Markdown syntax.
5. **Indentation**: Preserve indentation using `&nbsp;`.
6. **Dollar signs**: Separate dollar signs (`$`) into their own cells. Duplicate the corresponding column header when spliting.
7. **Brackets**: Merge brackets and their contents into a single cell.
8. **Content fidelity**: Do not modify any table content.
9. **Table legibility**: Ensure each row has same number of columns.
"""


def call_api(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {"role": "developer", "content": INSTRUCTION},
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": f"data:image/png;base64,{base64_image}",
                        "detail": "high",
                    },
                ],
            },
        ],
    )

    # print(response.usage)
    img = cv2.imread(image_path, 0)
    # print(gpt41_high_detail_token_cost(img.shape[1], img.shape[0]) + 44)
    return response.output_text


if __name__ == "__main__":
    with open("result.md", "w") as f:
        f.write(
            call_api("test/test_output/10-K/brka-20241231/table_113.png")
            .strip()
            .strip("\n")
            .strip("```markdown")
            .strip("```")
        )
    print(
        cal_2d_lev(
            read_md("result.md"),
            read_md("test/test_output/10-K/brka-20241231/table_113.md"),
        )
    )
