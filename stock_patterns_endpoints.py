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

class Standard_W_Pattern(object):
    """docstring for Standard_W_Pattern"""
    def __init__(self):
        super(Standard_W_Pattern, self).__init__()

    @classmethod
    def vectors(cls, Q1=None, P1=None, Q2=None, P2=None, Q3=None):
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

        cls.O_, cls.OQ2, cls.OQ1, cls.OP1, cls.OP2, cls.OQ3 = O_, OQ2, OQ1, OP1, OP2, OQ3,
        cls.P2Q2, cls.P1Q2, cls.P1Q1, cls.P2Q3, cls.P1P2 = P2Q2, P1Q2, P1Q1, P2Q3, P1P2
        cls.Q1Q3, cls.Q2O = Q1Q3, Q2O
        cls.c1, cls.c2 = c1, c2
        cls.P1Q1_, cls.P2Q3_ = P1Q1_, P2Q3_
        cls.v1, cls.v2 = v1, v2

    @classmethod
    def fuzzy_shapes(cls, P1P2=None, Q1Q3=None, Q2O=None):
        cos_01 = (
            (
                P1P2[0] * Q1Q3[0] + P1P2[1] * Q1Q3[1]
            ) /
            (
                math.sqrt(P1P2[0] ** 2 + P1P2[1] ** 2) *
                math.sqrt(Q1Q3[0] ** 2 + Q1Q3[1] ** 2)
            )
        )
        cos_02 = (
            (
                Q2O[0] * P1P2[0] + Q2O[1] * P1P2[1]
            ) /
            (
                math.sqrt(Q2O[0] ** 2 + Q2O[1] ** 2) *
                math.sqrt(P1P2[0] ** 2 + P1P2[1] ** 2)
            )
        )

        cls.cos_01 = cos_01
        cls.cos_02 = cos_02

    @classmethod
    def conditions(cls, cos_01=None, cos_02=None):
        """
        Pattern is a W shape if it satisfies the following properties.
        1. P1P2 || Q1Q2
        2. OQ2  ⊥ P1P2
        3. P1Q1 || P2Q2
        4. P1Q2 || P2Q3
        5. Q1, Q3 have approximately the same height
        6. P1, P2 have approximately the same height
        7. Q2 has a lower height than Q1 and Q3
        """
        if (
            np.isclose(
                [cos_01], 1, atol=0.001
            ).any() is np.bool_(True) and
            np.isclose(
                [cos_02], 0, atol=0.001
            ).any() is np.bool_(True)
        ):
            cls.status = True
        else:
            cls.status = False

        """
            plt.plot([Q1[0], P1[0], Q2[0], P2[0], Q3[0]], [Q1[1], P1[1], Q2[1], P2[1], Q3[1]])
            plt.show()
        """


    # def vectors --------------------------------------------------------------------------
    @classmethod
    def O_(cls):
        return cls.O_
    @classmethod
    def OQ2(cls):
        return cls.OQ2
    @classmethod
    def OQ1(cls):
        return cls.OQ1
    @classmethod
    def OP1(cls):
        return cls.OP1
    @classmethod
    def OP2(cls):
        return cls.OP2
    @classmethod
    def OQ3(cls):
        return cls.OQ3
    @classmethod
    def P2Q2(cls):
        return cls.P2Q2
    @classmethod
    def P1Q2(cls):
        return cls.P1Q2
    @classmethod
    def P1Q1(cls):
        return cls.P1Q1
    @classmethod
    def P2Q3(cls):
        return cls.P2Q3
    @classmethod
    def P1P2(cls):
        return cls.P1P2
    @classmethod
    def Q1Q3(cls):
        return cls.Q1Q3
    @classmethod
    def Q2O(cls):
        return cls.Q2O
    @classmethod
    def c1(cls):
        return cls.c1
    @classmethod
    def c2(cls):
        return cls.c2
    @classmethod
    def P1Q1_(cls):
        return cls.P1Q1_
    @classmethod
    def P2Q3_(cls):
        return cls.P2Q3_
    @classmethod
    def v1(cls):
        return cls.v1
    @classmethod
    def v2(cls):
        return cls.v2
    # --------------------------------------------------------------------------------------

    # def fuzzy_shapes ---------------------------------------------------------------------
    @classmethod
    def cos_01(cls):
        return cls.cos_01

    @classmethod
    def cos_02(cls):
        return cls.cos_02   
    # --------------------------------------------------------------------------------------       

    # def conditions -----------------------------------------------------------------------
    @classmethod
    def status(cls):
        return cls.status 
    # --------------------------------------------------------------------------------------  