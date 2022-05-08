import numpy as np


class Bond:
    coupon_frequency_dict = {'每年': 1, '每半年': 2, '每季度': 4, '每月': 12, '连续复利': 1000}

    def __init__(self, coupon_frequency, face_value, years_to_maturity, coupon_rate, market_rate):
        self.coupon_frequency = coupon_frequency
        self.face_value = face_value
        self.years_to_maturity = years_to_maturity
        self.coupon_rate = coupon_rate
        self.market_rate = market_rate
        self.number_of_coupons_in_one_year = self.coupon_frequency_dict[coupon_frequency]
        self.discount_rate_in_each_period = market_rate / self.number_of_coupons_in_one_year
        self.coupon_in_each_period = (self.face_value * self.coupon_rate / self.number_of_coupons_in_one_year) / 100
        self.number_of_coupons = int(self.years_to_maturity * self.number_of_coupons_in_one_year)
        self.v = self.years_to_maturity % (1 / self.number_of_coupons_in_one_year)  # 下一个付息日距离今天的间隔

    def cash_flow(self):
        cf = np.array([self.coupon_in_each_period] * int(self.number_of_coupons))
        cf[-1] += self.face_value
        # 若下一个付息日距离今天的间隔小于一个付息周期（即 v 大于0），则需要对现金流加上一个票息
        if (self.v - 0) > 1e-6:
            cf = np.insert(cf, 0, self.coupon_in_each_period)
        return cf

    def discount_factor(self):
        df = np.fromfunction(lambda i: 1 / (1 + self.discount_rate_in_each_period / 100) ** (i + 1),
                             (self.number_of_coupons,))
        # 若下一个付息日距离今天的间隔小于一个付息周期（即 v 大于0），则需要对折现因子加上一个1，再对所有的折现因子缩小，缩小的幅度为一个付息周期的折现因子
        if (self.v - 0) > 1e-6:
            df = np.insert(df, 0, 1)
            df = df * (1 / (1 + self.discount_rate_in_each_period / 100) ** self.v)
        return df

    def price(self):
        pv_of_cash_flow = np.dot(self.cash_flow(), self.discount_factor())
        return pv_of_cash_flow

    def macaulay_weight(self):
        mw = np.zeros(shape=(self.cash_flow().shape[0],))
        y = self.discount_rate_in_each_period / 100
        # 若下一个付息日距离今天的间隔小于一个付息周期（即 v 大于0），则每个现金流距离今天的间隔都不恰好是一个付息周期，需要加上一个付息周期的部分，即 self.v
        if (self.v - 0) > 1e-6:
            for i in range(mw.shape[0]):
                t = i / self.number_of_coupons_in_one_year + self.v
                mw[i] = t / ((1 + y) ** t)
        else:
            for i in range(mw.shape[0]):
                t = (1 + i) / self.number_of_coupons_in_one_year
                mw[i] = t / ((1 + y) ** (1 + i))
        return mw

    def macaulay_duration(self):
        # 根据麦考利久期公式，计算麦考利久期
        return np.dot(self.macaulay_weight(), self.cash_flow()) / self.price()

    def modified_duration(self):
        # 根据修正久期公式，计算修正久期
        y = self.discount_rate_in_each_period / 100
        return self.macaulay_duration() / (1 + y)

    def convexity_weight(self):
        cw = np.zeros(shape=(self.cash_flow().shape[0],))
        y = self.discount_rate_in_each_period / 100
        # 若下一个付息日距离今天的间隔小于一个付息周期（即 v 大于0），则每个现金流距离今天的间隔都不恰好是一个付息周期，需要加上一个付息周期的部分，即 self.v
        if (self.v - 0) > 1e-6:
            for i in range(cw.shape[0]):
                t = i / self.number_of_coupons_in_one_year + self.v
                cw[i] = t*(t+1/ self.number_of_coupons_in_one_year) / ((1 + y) ** (t + 2))
        else:
            for i in range(cw.shape[0]):
                t = (1 + i) / self.number_of_coupons_in_one_year
                cw[i] = t*(t+1/ self.number_of_coupons_in_one_year) / ((1 + y) ** (1 + i + 2))
        return cw

    def convexity(self):
        # 根据凸性公式，计算凸性
        return np.dot(self.convexity_weight(), self.cash_flow()) / self.price()
