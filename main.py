import functions
import importlib
import streamlit as st

importlib.reload(functions)
from functions import *

st.title('债券计算器')

st.sidebar.header('输入债券信息')
compounding_frequency = st.sidebar.selectbox('付息频率 Coupon Frequency', ['每年', '每半年', '每季度', '每月'])
face_value = st.sidebar.number_input(label='面值（元） Face Value', value=100.0, step=1.0, format='%f')
years_to_maturity = st.sidebar.number_input(label='到期年限（年） Years to Maturity', value=10.0, step=1.0, format='%f')
coupon_rate = st.sidebar.number_input(label='票息率（%） Coupon Rate', value=10.0, step=1.0, format='%f')
market_rate = st.sidebar.number_input(label='到期收益率（%）  Yield Rate', value=10.0, step=1.0, format='%f')

bond = Bond(compounding_frequency, face_value, years_to_maturity, coupon_rate, market_rate)

st.markdown('''
|| 计算公式| 计算结果 |
| -------------- | ------------------------------------------------------------ | -------- |
|**价格**| $P=\sum_{{t=1}}^{{T}} \\frac{{C F_{{t}}}}{{(1+y)^{{t}}}}$               |     {:.4f}     |
| **麦考利久期** | $D=\sum_{{t=1}}^{{T}} t \\times \\frac{{C F_{{t}}}}{{(1+y)^{{t}} P}}$      |   {:.4f}       |
| **修正久期**   | $D^{{*}}=\\frac{{D}}{{1+y}}$                                        |     {:.4f}     |
| **凸性**       | $C=\sum_{{t=1}}^{{T}} t(t+1) \\times \\frac{{C F_{{t}}}}{{(1+y)^{{t+2}} P}}$ |   {:.4f}       |
'''.format(bond.price(), bond.macaulay_duration(), bond.modified_duration(), bond.convexity())
            )
