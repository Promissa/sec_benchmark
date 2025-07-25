from src.html_parse import *
from src.doubao_api import call_api
import os

input_dir = "data/sec_samples/"
output_path = "test/test_output/html_parse/"


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
    files = list(find_html_files(input_dir, max_depth=2))
    for dirpath, fname in files:
        rel = os.path.relpath(dirpath, input_dir)
        base, _ = os.path.splitext(fname)
        ind = os.path.join(dirpath, fname)
        outd = os.path.join(output_path, rel, base)
        os.makedirs(outd, exist_ok=True)
        parse(ind, outd, type="csv")


if __name__ == "__main__":
    main()
