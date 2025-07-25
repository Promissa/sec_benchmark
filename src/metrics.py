import csv
import numpy as np
from zss import Node, simple_distance


def read_csv(file_path):
    table = []
    with open(file_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            table.append(row)
    return table


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

    def judge(s1, s2, ignoreComma=False):
        # `ignoreComma`: "123,456.789" "123456.789" will be taken equally when True
        if s1 == s2:
            return True
        if ignoreComma == False:
            return False
        if s1 == "" or s2 == "":
            return False
        if not all(char.isdigit() or char == "," or char == "." for char in s1):
            return False
        if not all(char.isdigit() or char == "," or char == "." for char in s2):
            return False
        return float(s1.replace(",", "")) == float(s2.replace(",", ""))

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
    n1, m1, n2, m2 = len(t1), len(t1[0]), len(t2), len(t2[0])
    f = np.zeros((n1 + 1, m1 + 1, n2 + 1, m2 + 1), dtype=int)
    for i in range(n1 + 1):
        f[i][0][0][0] = i
    for j in range(m1 + 1):
        f[0][j][0][0] = j
    for k in range(n2 + 1):
        f[0][0][k][0] = k
    for l in range(m2 + 1):
        f[0][0][0][l] = l
    for i in range(n1 + 1):
        for j in range(m1 + 1):
            f[i, j, 0, :] = min(i, j)
            f[i, j, :, 0] = min(i, j)
    for k in range(n2 + 1):
        for l in range(m2 + 1):
            f[:, 0, k, l] = min(k, l)
            f[0, :, k, l] = min(k, l)

    row_ed = np.zeros((n1, n2, m1 + 1, m2 + 1), dtype=int)
    col_ed = np.zeros((m1, m2, n1 + 1, n2 + 1), dtype=int)

    for i in range(n1):
        for j in range(n2):
            row_ed[i][j] = cal_lev(t1[i], t2[j])

    t1 = np.transpose(t1)
    t2 = np.transpose(t2)

    for i in range(m1):
        for j in range(m2):
            col_ed[i][j] = cal_lev(t1[i], t2[j])

    t1 = np.transpose(t1)
    t2 = np.transpose(t2)

    # 无法确定 行/列 删除的连续性
    for i in range(1, n1 + 1):
        for j in range(1, m1 + 1):
            for k in range(1, n2 + 1):
                for l in range(1, m2 + 1):
                    f[i][j][k][l] = min(
                        f[i - 1][j][k][l] + 1,
                        f[i][j - 1][k][l] + 1,
                        f[i][j][k - 1][l] + 1,
                        f[i][j][k][l - 1] + 1,
                        f[i - 1][j][k - 1][l] + row_ed[i - 1][k - 1][j][l],
                        f[i][j - 1][k][l - 1] + col_ed[j - 1][l - 1][i][k],
                    )

    return f


if __name__ == "__main__":
    # file1 = "data/parsed_table/1800_000110465911061064_10-Q_1800_1/table_4_2_a2.csv"
    # file2 = "data/parsed_table/1800_000110465911061064_10-Q_1800_1/table_4.csv"
    # print_table(read_csv("parsedtable/1800_000110465911061064_10-Q_1800_1/table_4_1.csv"))
    file1, file2 = (
        "test/benchmark_sample/parsed_result/sample.csv",
        "test/benchmark_sample/ground_truth/sample.csv",
    )
    # teds_test()
    # print(cal_2d_lev(read_csv(file1), read_csv(file2)))
    # print(cal_2d_zss(read_csv(file1), read_csv(file2)))
