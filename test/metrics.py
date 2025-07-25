from src.metrics import *
from table_recognition_metric import TEDS


csv_file1 = "test/test_input/metrics_sample/ground_truth/sample.csv"
csv_file2 = "test/test_input/metrics_sample/parsed_result/sample.csv"


def teds_test():
    teds = TEDS()
    gt_html = """
    <html><body>
    <table>
    <thead>
        <tr>
            <th></th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
            <th>Year ended March 31,</th>
        </tr>
        <tr>
            <th></th>
            <th>2022</th>
            <th>2022</th>
            <th>2022</th>
            <th>2023</th>
            <th>2023</th>
            <th>2023</th>
            <th>2024</th>
            <th>2024</th>
            <th>2024</th>
        </tr>
        <tr>
            <th></th>
            <th>Average balance</th>
            <th>Interest revenue/expense</th>
            <th>Average yield/cost</th>
            <th>Average balance</th>
            <th>Interest revenue/expense</th>
            <th>Average yield/cost</th>
            <th>Average balance</th>
            <th>Interest revenue/expense</th>
            <th>Average yield/cost</th>
        </tr>
        <tr>
            <td></td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
            <td>(in millions, except percentages)</td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Assets:</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Interest-earning assets:</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Cash and due from banks, and restricted cash</td>
            <td>Rs. 108,184.0</td>
            <td>Rs. 1,090.9</td>
            <td>1.0%</td>
            <td>Rs. 152,848.2</td>
            <td>Rs. 6,308.7</td>
            <td>4.1%</td>
            <td>Rs. 267,249.0</td>
            <td>Rs. 17,771.7</td>
            <td>6.6%</td>
        </tr>
        <tr>
            <td>Investments available for sale debt securities</td>
            <td>4,132,605.2</td>
            <td>240,943.0</td>
            <td>5.8</td>
            <td>4,875,942.8</td>
            <td>304,566.7</td>
            <td>6.2</td>
            <td>7,721,061.2</td>
            <td>516,550.0</td>
            <td>6.7</td>
        </tr>
        <tr>
            <td>Investments held for trading</td>
            <td>81,809.4</td>
            <td>1,647.5</td>
            <td>2.0</td>
            <td>71,944.9</td>
            <td>2,964.6</td>
            <td>4.1</td>
            <td>406,211.0</td>
            <td>3,563.1</td>
            <td>0.9</td>
        </tr>
        <tr>
            <td>Loans, net:</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td>Retail loans</td>
            <td>8,014,536.7</td>
            <td>807,146.1</td>
            <td>10.1</td>
            <td>9,863,886.2</td>
            <td>987,975.9</td>
            <td>10.0</td>
            <td>16,069,363.9</td>
            <td>1,625,134.5</td>
            <td>10.1</td>
        </tr>
        <tr>
            <td>Wholesale loans</td>
            <td>4,161,213.2</td>
            <td>250,779.5</td>
            <td>6.0</td>
            <td>5,173,660.0</td>
            <td>363,842.1</td>
            <td>7.0</td>
            <td>6,782,949.1</td>
            <td>569,391.0</td>
            <td>8.4</td>
        </tr>
        <tr>
            <td>Securities purchased with agreement to resell</td>
            <td>699,778.0</td>
            <td>25,101.0</td>
            <td>3.6</td>
            <td>52,860.0</td>
            <td>2,222.7</td>
            <td>4.2</td>
            <td>103,522.0</td>
            <td>4,276.9</td>
            <td>4.1</td>
        </tr>
        <tr>
            <td>Other assets</td>
            <td>278,018.3</td>
            <td>6,429.0</td>
            <td>2.3</td>
            <td>661,363.0</td>
            <td>21,646.0</td>
            <td>3.3</td>
            <td>1,088,516.4</td>
            <td>45,239.0</td>
            <td>4.2</td>
        </tr>
        <tr>
            <td>Total interest-earning assets:</td>
            <td>Rs. 17,476,144.8</td>
            <td>Rs. 1,333,137.0</td>
            <td>7.6%</td>
            <td>Rs. 20,852,505.1</td>
            <td>Rs. 1,689,526.7</td>
            <td>8.1%</td>
            <td>Rs. 32,438,872.6</td>
            <td>Rs. 2,781,926.2</td>
            <td>8.6%</td>
        </tr>
    </tbody>
</table>

</body></html>

    """

    pred_html = """
    <html><body>
    <table>
    <thead></thead>
    <tbody>
        <tr>
            <td style="text-align: left"></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
            <td style="text-align: left"><strong>Year ended March 31,</strong></td>
        </tr>
        <tr>
            <td style="text-align: left"></td>
            <td style="text-align: left"><strong>2022</strong></td>
            <td style="text-align: left"><strong>2022</strong></td>
            <td style="text-align: left"><strong>2022</strong></td>
            <td style="text-align: left"><strong>2022</strong></td>
            <td style="text-align: left"><strong>2022</strong></td>
            <td style="text-align: left"><strong>2023</strong></td>
            <td style="text-align: left"><strong>2023</strong></td>
            <td style="text-align: left"><strong>2023</strong></td>
            <td style="text-align: left"><strong>2023</strong></td>
            <td style="text-align: left"><strong>2023</strong></td>
            <td style="text-align: left"><strong>2024</strong></td>
            <td style="text-align: left"><strong>2024</strong></td>
            <td style="text-align: left"><strong>2024</strong></td>
            <td style="text-align: left"><strong>2024</strong></td>
            <td style="text-align: left"><strong>2024</strong></td>
        </tr>
        <tr>
            <td style="text-align: left"></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Average yield/ cost</strong></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Average yield/ cost</strong></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Average balance</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Interest revenue/ expense</strong></td>
            <td style="text-align: left"><strong>Average yield/ cost</strong></td>
        </tr>
        <tr>
            <td style="text-align: left"></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
            <td style="text-align: left"><strong>(in millions, except percentages)</strong></td>
        </tr>
        <tr>
            <td style="text-align: left"><strong>Assets:</strong></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
        </tr>
        <tr>
            <td style="text-align: left">Interest-earning assets:</td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
        </tr>
        <tr>
            <td style="text-align: left">Cash and due from banks, and restricted cash</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">108184.0</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">1090.9</td>
            <td style="text-align: left">1.0%</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">152848.2</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">6308.7</td>
            <td style="text-align: left">4.1%</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">267249.0</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">17771.7</td>
            <td style="text-align: left">6.6%</td>
        </tr>
        <tr>
            <td style="text-align: left">Investments available for sale debt securities</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">4132605.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">240943.0</td>
            <td style="text-align: left">5.8</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">4875942.8</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">304566.7</td>
            <td style="text-align: left">6.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">7721061.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">516550.0</td>
            <td style="text-align: left">6.7</td>
        </tr>
        <tr>
            <td style="text-align: left">Investments held for trading</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">81809.4</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">1647.5</td>
            <td style="text-align: left">2.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">71944.9</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">2964.6</td>
            <td style="text-align: left">4.1</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">406211.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">3563.1</td>
            <td style="text-align: left">0.9</td>
        </tr>
        <tr>
            <td style="text-align: left">Loans, net:</td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
            <td style="text-align: left"></td>
        </tr>
        <tr>
            <td style="text-align: left">Retail loans</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">8014536.7</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">807146.1</td>
            <td style="text-align: left">10.1</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">9863886.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">987975.9</td>
            <td style="text-align: left">10.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">16069363.9</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">1625134.5</td>
            <td style="text-align: left">10.1</td>
        </tr>
        <tr>
            <td style="text-align: left">Wholesale loans</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">4161213.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">250779.5</td>
            <td style="text-align: left">6.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">5173660.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">363842.1</td>
            <td style="text-align: left">7.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">6782949.1</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">569391.0</td>
            <td style="text-align: left">8.4</td>
        </tr>
        <tr>
            <td style="text-align: left">Securities purchased with agreement to resell</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">699778.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">25101.0</td>
            <td style="text-align: left">3.6</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">52860.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">2222.7</td>
            <td style="text-align: left">4.2</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">103522.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">4276.9</td>
            <td style="text-align: left">4.1</td>
        </tr>
        <tr>
            <td style="text-align: left">Other assets</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">278018.3</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">6429.0</td>
            <td style="text-align: left">2.3</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">661363.0</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">21646.0</td>
            <td style="text-align: left">3.3</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">1088516.4</td>
            <td style="text-align: left"></td>
            <td style="text-align: left">45239.0</td>
            <td style="text-align: left">4.2</td>
        </tr>
        <tr>
            <td style="text-align: left"><strong>Total interest-earning assets:</strong></td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">17476144.8</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">1333137.0</td>
            <td style="text-align: left">7.6%</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">20852505.1</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">1689526.7</td>
            <td style="text-align: left">8.1%</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">32438872.6</td>
            <td style="text-align: left">Rs.</td>
            <td style="text-align: left">2781926.2</td>
            <td style="text-align: left">8.6%</td>
        </tr>
    </tbody>
</table>
</body></html>
    """
    score = teds(gt_html, pred_html)
    print(f"TEDS 相似度分数: {score}")


# csv_file1 = "data/parsed_table/1800_000110465911061064_10-Q_1800_1/table_4_2_a2.csv"
# csv_file2 = "data/parsed_table/1800_000110465911061064_10-Q_1800_1/table_4.csv"
res = cal_ted(read_csv(csv_file1), read_csv(csv_file2))
print(res)
