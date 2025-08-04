from src.html_parse import *
from src.doubao_api import call_api
import os, tiktoken, base64, cv2
from math import ceil

input_dir = "data/sec_samples/"
output_path = "test/test_output/"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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


def find_png_files(root, max_depth=2):
    for dirpath, dirnames, filenames in os.walk(root):
        rel = os.path.relpath(dirpath, root)
        depth = 0 if rel == "." else rel.count(os.sep) + 1
        if depth > max_depth:
            dirnames[:] = []
            continue
        for fn in filenames:
            if fn.lower().endswith((".png")):
                yield dirpath, fn


def main():
    # files = list(find_html_files(input_dir, max_depth=2))
    # for dirpath, fname in files:
    #     rel = os.path.relpath(dirpath, input_dir)
    #     base, _ = os.path.splitext(fname)
    #     ind = os.path.join(dirpath, fname)
    #     outd = os.path.join(output_path, rel, base)
    #     os.makedirs(outd, exist_ok=True)
    #     parse(ind, outd)
    res = 0
    files = list(find_png_files(output_path, max_depth=2))
    for dirpath, fname in files:
        ind = os.path.join(dirpath, fname)
        with open(ind, "r") as f:
            md_str = str(f.read())
        res += len(tiktoken.get_encoding("cl100k_base").encode(md_str)) + 44
    print(res)


def gpt41_high_detail_token_cost(width: int, height: int) -> int:
    BASE_TOKENS = 85
    TILE_TOKENS = 170

    # Step 1: scale to fit within 2048x2048
    scale1 = min(2048 / width, 2048 / height, 1.0)
    w1, h1 = width * scale1, height * scale1

    # Step 2: scale so shortest side becomes 768
    shortest = min(w1, h1)
    scale2 = 768 / shortest
    final_w, final_h = w1 * scale2, h1 * scale2

    # Step 3: calculate number of 512x512 tiles
    tiles_w = ceil(final_w / 512)
    tiles_h = ceil(final_h / 512)
    num_tiles = tiles_w * tiles_h

    return BASE_TOKENS + TILE_TOKENS * num_tiles


if __name__ == "__main__":
    main()
