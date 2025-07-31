import os, io, base64, time
from volcenginesdkarkruntime import Ark  # pyright: ignore[reportMissingImports]
from src.html_parse import *

start = time.time()


def call_api(html: str) -> str:
    client = Ark(
        base_url="https://ark-cn-beijing.bytedance.net/api/v3",
        api_key=os.environ.get("ARK_API_KEY"),
        timeout=600,
    )
    response = client.chat.completions.create(
        model="ep-20250729115406-crwd9",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        # "text": "Extract the column header hierarchy into tree structure and specify the number of columns contained in each leaves, noted to recognize sign as an isolated column. Only output the result in form of a markdown-styled tree with column numbers at each leaf."
                        "text": "Extract the table contents into csv and keep the indent using space. Duplicate the cells with colspan and only output the result."
                        + html,
                    },
                ],
            },
        ],
        thinking={
            "type": "enabled",
        },
        extra_headers={"x-is-encrypted": "true"},
    )
    return response.choices[0].message.content


def find_html_files(root, max_depth=2):
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth > max_depth:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.lower().endswith((".html", ".htm")):
                yield dirpath, fn


def main():
    input_dir = "data/sec_samples/"
    output_path = "test/test_output/html_parse/"
    files = list(find_html_files(input_dir, max_depth=2))
    for dirpath, fname in files:
        rel = os.path.relpath(dirpath, input_dir)
        base, _ = os.path.splitext(fname)
        ind = os.path.join(dirpath, fname)
        outd = os.path.join(output_path, rel, base)
        os.makedirs(outd, exist_ok=True)
        tables = BeautifulSoup(read_html(ind), "html.parser").find_all("table")
        for i, table in enumerate(tables):
            with open(os.path.join(outd, f"table_{i}.md"), "w") as f:
                f.write(call_api(str(table)))
            print(f"Finished: table_{i}")
            time.sleep(10)


if __name__ == "__main__":
    main()
