import numpy as np
import pandas as pd

trade_df = pd.read_csv('data/2018-05-trade.csv')
trade_0501_df = trade_df[(trade_df['timestamp'] >= '2018-05-01') & (trade_df['timestamp'] < '2018-05-02')]
trade_0502_df = trade_df[(trade_df['timestamp'] >= '2018-05-02') & (trade_df['timestamp'] < '2018-05-03')]

order_book_0501_df = pd.read_csv('data/2018-05-01-orderbook.csv')
order_book_0501_df['timestamp'] = order_book_0501_df['timestamp'].astype('datetime64[s]')
order_book_0502_df = pd.read_csv('data/2018-05-02-orderbook.csv')
order_book_0502_df['timestamp'] = order_book_0502_df['timestamp'].astype('datetime64[s]')

order_0501_arr = []
order_0502_arr = []

# 0501 Processing
for index, item in trade_0501_df.iterrows():
    orders = order_book_0501_df[order_book_0501_df['timestamp'] == item['timestamp']]

    ask_orders = orders[orders['type'] == 1]
    ask_orders = ask_orders.sort_values(by=['price'], axis=0, ascending=False)
    bid_orders = orders[orders['type'] == 0]
    bid_orders = bid_orders.sort_values(by=['price'], axis=0)

    mid_price = np.mean(np.array([bid_orders.iloc[0]['price'], ask_orders.iloc[0]['price']]))

    ask_qty = ask_orders['quantity'].mean()
    bid_qty = bid_orders['quantity'].mean()

    ask_px = ask_orders['price'].mean()
    bid_px = bid_orders['price'].mean()

    book_price = (((ask_qty * bid_px) / bid_qty) + ((bid_qty * ask_px) / ask_qty)) / (bid_qty + ask_qty)
    book_feature = (book_price - mid_price)

    row = [item['timestamp'], item['price'], mid_price, book_feature, item['side']]
    order_0501_arr.append(row)

# 0502 Processing
for index, item in trade_0502_df.iterrows():
    orders = order_book_0502_df[order_book_0502_df['timestamp'] == item['timestamp']]

    ask_orders = orders[orders['type'] == 1]
    ask_orders = ask_orders.sort_values(by=['price'], axis=0, ascending=False)
    bid_orders = orders[orders['type'] == 0]
    bid_orders = bid_orders.sort_values(by=['price'], axis=0)

    mid_price = np.mean(np.array([bid_orders.iloc[0]['price'], ask_orders.iloc[0]['price']]))

    ask_qty = ask_orders['quantity'].mean()
    bid_qty = bid_orders['quantity'].mean()

    ask_px = ask_orders['price'].mean()
    bid_px = bid_orders['price'].mean()

    book_price = (((ask_qty * bid_px) / bid_qty) + ((bid_qty * ask_px) / ask_qty)) / (bid_qty + ask_qty)
    book_feature = (book_price - mid_price)

    row = [item['timestamp'], item['price'], mid_price, book_feature, item['side']]
    order_0502_arr.append(row)

order_0501_df = pd.DataFrame(order_0501_arr, columns=['timestamp', 'price', 'mid_price', 'book_feature', 'side'])
order_0502_df = pd.DataFrame(order_0502_arr, columns=['timestamp', 'price', 'mid_price', 'book_feature', 'side'])

frames = [order_0501_df, order_0502_df]
new_trade_df = pd.concat(frames)
new_trade_df = new_trade_df.reset_index(drop=True)
new_trade_df.to_csv('2018-05-trade-new.csv')
