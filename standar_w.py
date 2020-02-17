from stock_patterns_endpoints import Stock_Info, Standard_W_Pattern
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
    print(count, end="\r")
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
        standard_w_pattern = Standard_W_Pattern()
        standard_w_vectors = standard_w_pattern.vectors(
            Q1=(row[0][0], row[0][1]),
            P1=(row[1][0], row[1][1]),
            Q2=(row[2][0], row[2][1]),
            P2=(row[3][0], row[3][1]),
            Q3=(row[4][0], row[4][1])
        )

        standard_w_fuzzy_shapes = standard_w_pattern.fuzzy_shapes(
            P1P2=standard_w_pattern.P1P2,
            Q1Q3=standard_w_pattern.Q1Q3,
            Q2O=standard_w_pattern.Q2O
        )

        standard_w_conditions = standard_w_pattern.conditions(
            cos_01=standard_w_pattern.cos_01,
            cos_02=standard_w_pattern.cos_02
        )

        # print(standard_w_pattern.status)
        