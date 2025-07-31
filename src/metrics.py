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


import heapq


def compute_mods(src, tgt, del_rows, del_cols):
    """
    After deleting rows in del_rows and columns in del_cols from src,
    compute the number of single-cell edits needed to match tgt.
    Assumes the resulting shape of src matches tgt exactly.
    """
    n2, m2 = len(tgt), len(tgt[0])
    keep_rows = [i for i in range(len(src)) if i not in del_rows]
    keep_cols = [j for j in range(len(src[0])) if j not in del_cols]

    # sanity check
    assert len(keep_rows) == n2 and len(keep_cols) == m2

    mods = 0
    for i2, i_src in enumerate(keep_rows):
        for j2, j_src in enumerate(keep_cols):
            if not same(src[i_src][j_src], tgt[i2][j2]):
                mods += 1
    return mods


def same(a, b):
    if a == b:
        return True
    try:
        return float(a.replace(",", "")) == float(b.replace(",", ""))
    except:
        return False


def ted_astar(src, tgt):
    """A* search over deletions, exploring all goal states to find minimal cost."""
    n1, m1 = len(src), len(src[0]) if src else 0
    n2, m2 = len(tgt), len(tgt[0]) if tgt else 0
    if n1 < n2 and m1 < m2:
        src, tgt = tgt, src
        n1, m1 = len(src), len(src[0]) if src else 0
        n2, m2 = len(tgt), len(tgt[0]) if tgt else 0

    if n1 < n2 or m1 < m2:
        return float("inf")

    R_d = n1 - n2  # rows to delete
    C_d = m1 - m2  # cols to delete

    def h(R, C):
        return (R_d - len(R)) + (C_d - len(C))

    start = (frozenset(), frozenset())
    goal_size = (R_d, C_d)

    # priority queue: (f = g + h, g, R_set, C_set)
    pq = [(h(frozenset(), frozenset()), 0, frozenset(), frozenset())]
    seen = {start: 0}
    best = float("inf")

    while pq:
        fcur, gcur, R, C = heapq.heappop(pq)
        # prune by current best total cost
        if fcur > best:
            break
        # if goal state, compute full cost and update best
        if (len(R), len(C)) == goal_size:
            total = gcur + compute_mods(src, tgt, R, C)
            if total < best:
                best = total
            continue
        # expand neighbors: delete a row
        if len(R) < R_d:
            for i in range(n1):
                if i not in R:
                    R2 = R | {i}
                    g2 = gcur + 1
                    state2 = (R2, C)
                    if g2 < seen.get(state2, float("inf")):
                        seen[state2] = g2
                        heapq.heappush(pq, (g2 + h(R2, C), g2, R2, C))
        # delete a column
        if len(C) < C_d:
            for j in range(m1):
                if j not in C:
                    C2 = C | {j}
                    g2 = gcur + 1
                    state2 = (R, C2)
                    if g2 < seen.get(state2, float("inf")):
                        seen[state2] = g2
                        heapq.heappush(pq, (g2 + h(R, C2), g2, R, C2))

    return best if best < float("inf") else compute_mods(src, tgt, set(), set())


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
