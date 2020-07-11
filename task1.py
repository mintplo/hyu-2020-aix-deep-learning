import numpy as np
import pandas as pd

pd.options.display.float_format = "{:,.4f}".format

trade_df = pd.read_csv("data/2018-05-trade.csv")

# == 데이터 준비 과정
# 1. 2018년 5월 1일부터 2일까지의 데이터를 필터
# 2. 소수점 4 digit 에서 반올림 처리
# 3. Quantity 누적 계산을 위한 처리
# 4. Quantity 누적 계산이 0이 될 때를 찾아 Profit 계산 => 저장
trade_df_in_2days = trade_df[(trade_df['timestamp'] >= '2018-05-01') & (trade_df['timestamp'] < '2018-05-03')]
trade_df_in_2days = trade_df_in_2days.round(4)
trade_df_in_2days['quantity_for_accum'] = trade_df_in_2days.apply(
    lambda x: x['quantity'] if x['side'] == 0 else x['quantity'] * -1, axis=1)
trade_df_in_2days['accumulative_quantity'] = trade_df_in_2days['quantity_for_accum'].cumsum()

profit_amount = 0
profit_amount_arr = []

for index, item in trade_df_in_2days.iterrows():
    profit_amount += item['amount']

    # Quantity 누적 계산이 0이 되는 시점이 Profit 이 되는 시점
    # The profit calculation moment should be when the accumulative quantity is 0
    # (only consider 4 digit floating number, ignore the rest).
    if round(item['accumulative_quantity'], 4) == 0.0:
        profit_amount_arr.append(profit_amount)
        profit_amount = 0


profit_amount_np_arr = np.array(profit_amount_arr)
# Profit 계산
print(np.sum(profit_amount_np_arr))
