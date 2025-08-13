import csv, io
import numpy as np
import pandas as pd
from zss import Node, simple_distance


def read_csv(file_path):
    table = []
    with open(file_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            table.append(row)
    return table


def read_md(file):
    with open(file, "r") as f:
        table_str = f.read()
    df = (
        pd.read_csv(io.StringIO(table_str), sep="|", index_col=1)
        .dropna(axis=1, how="all")
        .iloc[1:]
    )
    return df.to_numpy().tolist()


def print_table(t):
    for i in range(len(t)):
        print(t[i])


def cal_lev(r1, r2):
    n, m = len(r1), len(r2)
    f = np.zeros((n + 1, m + 1), dtype=int)

    for i in range(n + 1):
        f[i][0] = i
    for j in range(m + 1):
        f[0][j] = j

    def judge(a, b, ignoreComma=False):
        if a == b:
            return True
        if ignoreComma:
            try:
                return float(a.replace(",", "")) == float(b.replace(",", ""))
            except:
                return False
        else:
            return False

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if judge(r1[i - 1], r2[j - 1]):
                f[i][j] = f[i - 1][j - 1]
            else:
                f[i][j] = min(f[i - 1][j] + 1, f[i][j - 1] + 1, f[i - 1][j - 1] + 1)
    return f


def cal_2d_lev(t1, t2):
    n, m = len(t1), len(t2)
    f = np.zeros((n + 1, m + 1), dtype=int)

    for i in range(n + 1):
        f[i][0] = i
    for j in range(m + 1):
        f[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = cal_lev(t1[i - 1], t2[j - 1])[len(t1[i - 1])][len(t2[j - 1])]
            f[i][j] = min(f[i - 1][j] + 1, f[i][j - 1] + 1, f[i - 1][j - 1] + cost)

    # print_table(f)
    return f[n][m]


def cal_ted(t1, t2):
    t1 = np.asarray(t1, dtype=object)
    t2 = np.asarray(t2, dtype=object)
    n1, m1 = t1.shape
    n2, m2 = t2.shape

    f = np.zeros((n1 + 1, m1 + 1, n2 + 1, m2 + 1), dtype=int)

    # Base: to/from empty tables
    for i in range(n1 + 1):
        for j in range(m1 + 1):
            f[i, j, 0, 0] = i + j
    for k in range(n2 + 1):
        for l in range(m2 + 1):
            f[0, 0, k, l] = k + l

    # Mixed bases (one dimension empty on target or source)
    for i in range(n1 + 1):
        for j in range(m1 + 1):
            for l in range(m2 + 1):
                f[i, j, 0, l] = i + abs(j - l)
    for i in range(n1 + 1):
        for j in range(m1 + 1):
            for k in range(n2 + 1):
                f[i, j, k, 0] = j + abs(i - k)

    row_ed = np.zeros((n1, n2, m1 + 1, m2 + 1), dtype=int)
    for i in range(n1):
        for k in range(n2):
            row_ed[i, k] = cal_lev(t1[i].tolist(), t2[k].tolist())

    col_ed = np.zeros((m1, m2, n1 + 1, n2 + 1), dtype=int)
    t1T, t2T = t1.T, t2.T
    for j in range(m1):
        for l in range(m2):
            col_ed[j, l] = cal_lev(t1T[j].tolist(), t2T[l].tolist())

    for i in range(1, n1 + 1):
        for j in range(1, m1 + 1):
            for k in range(1, n2 + 1):
                for l in range(1, m2 + 1):
                    f[i, j, k, l] = min(
                        f[i - 1, j, k, l] + 1,
                        f[i, j - 1, k, l] + 1,
                        f[i, j, k - 1, l] + 1,
                        f[i, j, k, l - 1] + 1,
                        f[i - 1, j, k - 1, l] + row_ed[i - 1, k - 1, j, l],
                        f[i, j - 1, k, l - 1] + col_ed[j - 1, l - 1, i, k],
                    )

    return f


if __name__ == "__main__":
    file1, file2 = (
        "test/test_input/metrics_sample/parsed_result/sample.csv",
        "test/test_input/metrics_sample/ground_truth/sample.csv",
    )
    print(cal_ted(read_csv(file1), read_csv(file2)))
