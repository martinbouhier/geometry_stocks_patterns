from stock_patterns_endpoints import Stock_Info, Geometry_Patters
from itertools import combinations


stock_test = Stock_Info(start='2019-09-01', end='2020-02-08', stock='BAC')
df = stock_test.get_stock_data()
df = df.reset_index()
df = stock_test.max_min_dataframe(df, 'Adj Close')
df_new = df[df['Close_status'] != '0']
df_new = df_new[['index', 'Adj Close', 'Close_status']]

count = 0
for row in combinations(df_new.values, 5):
    count += 1
    print(count)
    if (
        row[0][2] == 'MAX' and
        row[1][2] == 'MIN' and
        row[2][2] == 'MAX' and
        row[3][2] == 'MIN' and
        row[4][2] == 'MAX'
    ):
        """
        Example perfect W
        Q1 = (1, 30)
        P1 = (2, 5)
        Q2 = (3, 20)
        P2 = (4, 5)
        Q3 = (5, 30)
        """
        Q1 = (row[0][0], row[0][1])
        P1 = (row[1][0], row[1][1])
        Q2 = (row[2][0], row[2][1])
        P2 = (row[3][0], row[3][1])
        Q3 = (row[4][0], row[4][1])

        geometry_patterns = Geometry_Patters()
        standard_w = geometry_patterns.geometric_definition_fuzzy_standard_w(Q1, P1, Q2, P2, Q3)
