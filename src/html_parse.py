import re, csv, os, tabulate, chardet, pdb
import pandas as pd
import numpy as np
from tqdm import tqdm
from bs4 import BeautifulSoup
from unstructured.cleaners.core import clean_extra_whitespace


def dict_sort(dict: dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in sorted(dict.items(), key=lambda item: item[1])}


def read_html(file_path: str) -> str:
    with open(file_path, "rb") as file:
        enc = chardet.detect(file.read())["encoding"]
    with open(file_path, "r", encoding=enc) as file:
        return file.read()


def write_csv(file_path: str, data: list[list[str]]):
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_style_attr(soup: BeautifulSoup, attr: str) -> str | None:
    def parse_style(style_str: str) -> dict[str, str]:
        styles: dict[str, str] = {}
        for decl in style_str.split(";"):
            if ":" in decl:
                prop, val = decl.split(":", 1)
                prop = prop.strip().lower()
                val = val.strip()
                if prop:
                    styles[prop] = val
        return styles

    merged_styles: dict[str, str] = {}

    if soup.get("style"):
        props = parse_style(soup.get("style"))
        merged_styles.update(props)

    for tag in ["p", "td", "span"]:
        for item in soup.find_all(tag):
            style_str = item.get("style")
            if not style_str:
                continue
            props = parse_style(style_str)
            merged_styles.update(props)

    top_level_divs = [d for d in soup.find_all("div") if d.find_parent("div") is None]
    if top_level_divs:
        current_div = top_level_divs[0]
        while current_div:
            style_str = current_div.get("style", "")
            if style_str:
                merged_styles.update(parse_style(style_str))
            children = [child for child in current_div.find_all("div", recursive=False)]
            current_div = children[0] if children else None

    try:
        return merged_styles[attr]
    except:
        return None


def get_indent(soup: BeautifulSoup) -> float:
    res_pt = 0.0
    for attr in ["margin-left", "margin", "text-indent", "padding-left"]:
        indent_str = get_style_attr(soup, attr)
        if indent_str is None:
            continue
        if attr == "margin":
            indent_str = indent_str.split(" ")[-1]
        if indent_str == "auto":
            continue
        indent_value = float(
            indent_str.replace("pt", "")
            .replace("em", "")
            .replace("px", "")
            .replace("in", "")
            .replace("%", "")
        )
        if "em" in indent_str:
            indent_value *= 16
        elif "in" in indent_str:
            indent_value *= 72
        elif "%" in indent_str:
            indent_value *= 7.2
        elif "pt" in indent_str and os.name == "nt":
            indent_value = indent_value * 4 / 3  # for 96dpi in windows
        res_pt += indent_value
    return res_pt


def replace_prefix(df: pd.DataFrame, prefix: str, replace: str = "nan") -> pd.DataFrame:
    escaped_prefix = re.escape(prefix)
    pattern = re.compile(f"^{escaped_prefix}*$")

    def replace_cell_to_nan(cell):
        if isinstance(cell, str) and re.match(pattern, cell):
            return np.nan
        return cell

    def replace_cell_to_space(cell):
        if isinstance(cell, str) and re.match(pattern, cell):
            return " "
        return cell

    if replace == "nan":
        return df.applymap(replace_cell_to_nan)
    elif replace == "space":
        return df.applymap(replace_cell_to_space)


def clean_table(
    table_contents: list[list[str]], row_ignored: list[int], prefix: str
) -> list[list[str]]:
    df = pd.DataFrame(table_contents)
    df_p = df.drop(index=row_ignored).replace("", np.nan)
    df_p = replace_prefix(df_p, prefix, replace="nan")
    if df_p.empty:
        return table_contents
    empty_rows = df_p.isna().all(axis=1)
    empty_cols = df_p.isna().all(axis=0)
    df = df.replace(np.nan, "")
    ret = []
    # print(df.index, df_p.index)
    for i in df.index:
        ret.append(df.loc[i, ~empty_cols].tolist())
    return ret


def detect_sec_type(html: str) -> str:
    candidates = set(re.findall(r"<TYPE>\s*([^\s<]+)", html.upper()))
    known_forms = ["10K", "10Q", "S1", "S3", "20F"]

    for form in known_forms:
        if form in candidates:
            return form

    return "__UNKNOWN__"


invalid_tags = [("<ix:header", "</ix:header>")]
remove_tags = [
    ("<ix:nonNumeric", ">"),
    ("</ix:nonNumeric", ">"),
    ("<ix:continuation", ">"),
    ("</ix:continuation", ">"),
]


def to_markdown_with_alignment(df: pd.DataFrame, alignments: str = "left", **kwargs):
    """
    Convert DataFrame to markdown with alignment.

    Parameters:
        df: pd.DataFrame
        alignments: list of 'left', 'center', or 'right' for each column
        kwargs: passed to df.to_markdown()

    Returns:
        str: Markdown table with aligned columns
    """
    markdown = df.to_markdown(index=kwargs.get("index", True), **kwargs)
    lines = markdown.splitlines()

    # Generate alignment line
    align_map = {"left": ":---", "center": ":---:", "right": "---:"}
    align_line = "| " + " | ".join(align_map.get(a, ":---") for a in alignments) + " |"

    # Replace second line with alignment line
    lines[1] = align_line

    return "\n".join(lines)


def parse(file_path: str, output_path: str, type: str = "md", min_row: int = 3):
    """
    Parse HTML file into multiple markdown/csv tables

    Parameters:
        file_path: path to the input HTML file
        output_path: path to the output directory
        type: output type, 'md' or 'csv'
        min_row: minimum number of rows for a table to be considered valid

    Returns:
        None
    """
    if (
        type not in ["md", "csv"]
        or not os.path.exists(file_path)
        or not os.path.exists(output_path)
    ):
        pass

    tables = BeautifulSoup(read_html(file_path), "html.parser").find_all("table")

    for it in invalid_tags:
        while it[0] in tables:
            id0 = tables.index(it[0])
            id1 = tables.index(it[1]) + len(it[1])
            tables = tables[:id0] + tables[id1:]
    for it in remove_tags:
        while it[0] in tables:
            id0 = tables.index(it[0])
            id1 = tables[id0:].index(it[1]) + len(it[1])
            tables = tables[:id0] + tables[id0 + id1 :]

    prev_table_contents = None
    table_idx = 0
    prefix = "&nbsp;"

    for table in tqdm(tables, desc="Parsing " + file_path, unit="table"):
        rows = BeautifulSoup(str(table), "html.parser").find_all("tr")
        table_contents = []
        indents_pt = []
        row_ignored = []
        for i, row in enumerate(rows):
            items = BeautifulSoup(str(row), "html.parser").find_all("td")
            table_contents.append([])
            indents_pt.append([])
            for item in items:
                # save contents
                item_str = (
                    " ".join(item.stripped_strings)
                    .replace("&nbsp;", " ")
                    .replace("<br>", " ")
                )
                item_str = item_str.replace("( ", "(").replace("’", "'")
                item_str = re.sub(r"(?<=\d),(?=\d)", "", item_str)  # 1,234 => 1234
                item_str = clean_extra_whitespace(item_str)
                if type == "md":
                    item_str = item_str.replace("*", "\*")
                # save bold/italic
                if item_str != "":
                    if get_style_attr(item, "font-weight") == "bold" or item.find("b"):
                        item_str = "**" + item_str + "**"
                    if get_style_attr(item, "font-style") == "italic":
                        item_str = "*" + item_str + "*"
                    if get_style_attr(item, "text-transform") == "uppercase":
                        item_str = item_str.upper()
                    elif get_style_attr(item, "text-transform") == "lowercase":
                        item_str = item_str.lower()

                if get_style_attr(item, "text-align") != "right":
                    table_contents[i].append(item_str)

                # colspan
                if item.get("colspan"):
                    row_ignored.append(i)
                    for _ in range(int(item.get("colspan")) - 1):
                        table_contents[i].append(item_str)
                        indents_pt[i].append(get_indent(item))

                if get_style_attr(item, "text-align") == "right":
                    table_contents[i].append(item_str)

                indents_pt[i].append(get_indent(item))

        indents_pt = list(map(list, zip(*indents_pt)))  # transposed

        # add indent
        for j, row_pt in enumerate(indents_pt):
            pt_set = sorted(list(set(row_pt)))
            if len(pt_set) == 1:
                continue
            for i in range(len(table_contents)):
                indent_str = prefix * 2 * pt_set.index(indents_pt[j][i])
                table_contents[i][j] = indent_str + table_contents[i][j]

        # table_contents = clean_table(table_contents, [], prefix)

        column_headers = []
        for i in range(len(table_contents)):
            if len(table_contents[i]) <= 1:
                continue
            if table_contents[i][0].replace(prefix, "") == "" and not all(
                table_contents[i][j].replace(prefix, "") == ""
                for j in range(1, len(table_contents[i]))
            ):
                column_headers.append(i)
            elif table_contents[i][0].replace(prefix, "") != "":
                break

        # add column headers to row_ignored list
        if len(column_headers) > 0:
            if column_headers[-1] < len(table_contents) - 1:
                row_ignored = list(set(row_ignored + column_headers))
        else:
            row_ignored = list(set(row_ignored))

        # table_contents = clean_table(table_contents, row_ignored, prefix)

        for i in range(len(table_contents)):
            for j in range(1, len(table_contents[i])):
                # pre sign
                if (
                    table_contents[i][j - 1].strip("*") in ["($", "("]
                    and table_contents[i][j] != table_contents[i][j - 1]
                ):
                    tmp = table_contents[i][j - 1].rstrip("*")
                    table_contents[i][j] = tmp + table_contents[i][j].lstrip("*")
                    table_contents[i][j - 1] = ""
                # post sign
                k = j - 1
                while k < len(table_contents[i]) - 1:
                    k += 1
                    if table_contents[i][k].strip(" ").strip("*") == "":
                        continue
                    elif (
                        table_contents[i][k].strip("*") in [")", "%", ")%", "%)"]
                        and i not in column_headers
                    ):
                        table_contents[i][j - 1] = table_contents[i][j - 1].rstrip(
                            "*"
                        ) + table_contents[i][k].lstrip("*")
                        table_contents[i][k] = ""
                    # (a) index case
                    elif (
                        re.match(r"\(.\)", table_contents[i][k].strip(" ").strip("*"))
                        and len(table_contents[i][j - 1]) > 1
                    ):
                        starcount = 0
                        if table_contents[i][j - 1][0] == "*":
                            starcount += 1
                        if table_contents[i][j - 1][1] == "*":
                            starcount += 1
                        table_contents[i][j - 1] = (
                            (
                                table_contents[i][j - 1].rstrip("*")
                                + table_contents[i][k].strip(" ").strip("*")
                                + "*" * starcount
                            )
                            if starcount > 0
                            else table_contents[i][j - 1] + table_contents[i][k]
                        )
                        table_contents[i][k] = ""
                    else:
                        break
                j = k + 1
            for j in range(1, len(table_contents[i]) - 1):
                # connection sign
                if table_contents[i][j].strip("*") in ["-"]:
                    table_contents[i][j] = ""
                    table_contents[i][j + 1] = (
                        table_contents[i][j - 1].rstrip("*")
                        + table_contents[i][j].strip("*")
                        + table_contents[i][j + 1].lstrip("*")
                    )
                    table_contents[i][j - 1] = ""

        table_contents = clean_table(table_contents, row_ignored, prefix)
        if prev_table_contents is None:
            prev_table_contents = table_contents
        if len(table_contents) == 1:
            try:
                if (
                    re.match(r"\(.\)", table_contents[0][0])
                    or table_contents[0][0].strip() == "*"
                ):
                    prev_table_contents = prev_table_contents + table_contents
            except:
                pass
        else:
            df = pd.DataFrame(prev_table_contents).replace(float("NaN"), "")
            df.replace("", np.nan, inplace=True)
            df.dropna(how="all", inplace=True)
            df.replace(np.nan, "", inplace=True)
            prev_table_contents = table_contents
            if len(df) < min_row:
                continue
            table_idx += 1
            if type == "md":
                print(f"Output table_{table_idx}")
                df = df.replace({"\$": r"\$"}, regex=True)
                df.to_markdown(
                    os.path.join(output_path, f"table_{table_idx}.md"), index=False
                )
            elif type == "csv":
                df = df.replace(to_replace="&nbsp;", value=" ")
                df.to_csv(
                    os.path.join(output_path, f"table_{table_idx}.csv"), index=False
                )
    if prev_table_contents:
        df = pd.DataFrame(prev_table_contents).replace(float("NaN"), "")
        if type == "md":
            df = df.replace({"\$": r"\$"}, regex=True)
            df.to_markdown(
                os.path.join(output_path, f"table_{table_idx + 1}.md"), index=False
            )
        elif type == "csv":
            df = df.replace(to_replace="&nbsp;", value=" ")
            df.to_csv(
                os.path.join(output_path, f"table_{table_idx + 1}.csv"), index=False
            )


if __name__ == "__main__":
    parse(
        "data/sec_samples/10-K/tsla-20241231.html",
        "test/test_output/html_parse/10-K/tsla-20241231/",
        type="md",
    )
