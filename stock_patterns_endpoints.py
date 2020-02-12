from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import datetime
import math
import numpy as np


class Stock_Info(object):
    """docstring for Stock_Info"""
    def __init__(self, start=None, end=None, stock=None):
        super(Stock_Info, self).__init__()
        self.start = datetime.datetime.strptime(start, '%Y-%m-%d')
        self.end = datetime.datetime.strptime(end, '%Y-%m-%d')
        self.stock = stock

    def get_stock_data(self):
        df = pdr.get_data_yahoo(self.stock, self.start, self.end)
        return df

    def max_min_dataframe(self, df, header):
        conditions = [
            (
                (df[header] > df[header].shift(-1)) &
                (df[header] > df[header].shift(1))
            ),
            (
                (df[header] < df[header].shift(-1)) &
                (df[header] < df[header].shift(1))
            )
        ]
        choices = ['MAX', 'MIN']
        df['Close_status'] = np.select(
            conditions,
            choices,
            default=0
        )
        df['index'] = df.index
        df = df[['index', 'Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Close_status']]
        return df

class Geometry_Patters(object):
    """docstring for Geometry_Patters"""
    def __init__(self):
        super(Geometry_Patters, self).__init__()

    def standard_w_pattern(self, Q1, P1, Q2, P2, Q3):
        O_ = (P1[0] + P2[0]) / 2, (P1[1] + P2[1]) / 2
        OQ2 = Q2[0] - O_[0], Q2[1] - O_[1]
        OQ1 = Q1[0] - O_[0], Q1[1] - O_[1]
        OP1 = P1[0] - O_[0], P1[1] - O_[1]
        OP2 = P2[0] - O_[0], P2[1] - O_[1]
        OQ3 = Q3[0] - O_[0], Q3[1] - O_[1]
        P2Q2 = OQ2[0] - OP2[0], OQ2[1] - OP2[1]
        P1Q2 = OQ2[0] + OP2[0], OQ2[1] + OP2[1]
        P1Q1 = OQ1[0] - OP1[0], OQ1[1] - OP1[1]
        P2Q3 = OQ3[0] - OP2[0], OQ3[1] - OP2[1]
        P1P2 = P2[0] - P1[0], P2[1] - P1[1]
        Q1Q3 = Q3[0] - Q1[0], Q3[1] - Q1[1]
        Q2O = O_[0] - Q2[0], O_[1] - Q2[1]
        longitude_P1Q1 = math.sqrt(P1Q1[0] ** 2 + P1Q1[1] ** 2)
        longitude_P2Q2 = math.sqrt(P2Q2[0] ** 2 + P2Q2[1] ** 2)
        c1 = longitude_P1Q1 / longitude_P2Q2
        longitude_P2Q3 = math.sqrt(P2Q3[0] ** 2 + P2Q3[1] ** 2)
        longitude_P2Q2 = math.sqrt(P1Q2[0] ** 2 + P1Q2[1] ** 2)
        c2 = longitude_P2Q3 / longitude_P2Q2
        P1Q1_ = OP1[0] + P2Q2[0] * c1, OP1[1] + P2Q2[1] * c1
        P2Q3_ = OP2[0] + P1Q2[0] * c2, OP2[1] + P1Q2[1] * c2
        v1 = OP2
        v2 = OQ2
        # ---------------------------------------------------------------------------------------------
        cos_01_part1 = (P1P2[0] * Q1Q3[0]) + (P1P2[1] * Q1Q3[1])
        cos_01_part2 = (math.sqrt(P1P2[0] ** 2 + P1P2[1] ** 2) * math.sqrt(Q1Q3[0] ** 2 + Q1Q3[1] ** 2))
        cos_01 = cos_01_part1 / cos_01_part2
        # ---------------------------------------------------------------------------------------------
        cos_02_part1 = (Q2O[0] * P1P2[0]) + (Q2O[1] * P1P2[1])
        cos_02_part2 = (math.sqrt(Q2O[0] ** 2 + Q2O[1] ** 2) * math.sqrt(P1P2[0] ** 2 + P1P2[1] ** 2))
        cos_02 = cos_02_part1 / cos_02_part2

        if (
            (c1 >= 1 and c2 >= 1) and
            np.isclose([cos_01], 1, atol=0.001).any() is np.bool_(True) and np.isclose([cos_02], 0, atol=0.001).any() is np.bool_(True)
        ):
            print(c1)
            print(c2)
            print(P1Q1, P1Q1_)
            print(P2Q3, P2Q3_)
            plt.plot([Q1[0], P1[0], Q2[0], P2[0], Q3[0]], [Q1[1], P1[1], Q2[1], P2[1], Q3[1]])
            plt.show()
            
