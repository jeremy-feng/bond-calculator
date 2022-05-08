import functions
import importlib
import streamlit as st

importlib.reload(functions)
from functions import *

st.title('债券计算器')

st.sidebar.header('债券参数设置')
compounding_frequency = st.sidebar.selectbox('付息频率', ['每年', '每半年', '每季度', '每月', '连续复利'])
face_value = st.sidebar.number_input(label='面值（元）', value=100.0, step=1.0, format='%f')
years_to_maturity = st.sidebar.number_input(label='到期年限（年）', value=10.0, step=1.0, format='%f')
coupon_rate = st.sidebar.number_input(label='票息率（%）', value=10.0, step=1.0, format='%f')
market_rate = st.sidebar.number_input(label='市场利率（%）', value=10.0, step=1.0, format='%f')

bond = Bond(compounding_frequency, face_value, years_to_maturity, coupon_rate, market_rate)

st.markdown('''
|| 计算公式| 计算结果 |
| -------------- | ------------------------------------------------------------ | -------- |
|**价格**| $P=\sum_{{t=1}}^{{T}} \\frac{{C F_{{t}}}}{{(1+y)^{{t}}}}$               |     {:.2f}     |
| **麦考利久期** | $D=\sum_{{t=1}}^{{T}} t \\times \\frac{{C F_{{t}}}}{{(1+y)^{{t}} P}}$      |   {:.2f}       |
| **修正久期**   | $D^{{*}}=\\frac{{D}}{{1+y}}$                                        |     {:.2f}     |
| **凸性**       | $C=\sum_{{t=1}}^{{T}} t(t+1) \\times \\frac{{C F_{{t}}}}{{(1+y)^{{t+2}} P}}$ |   {:.2f}       |
'''.format(bond.price(), bond.macaulay_duration(), bond.modified_duration(), bond.convexity())
            )

