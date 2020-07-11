import pandas as pd
import matplotlib.pyplot as plt

trade_df = pd.read_csv("data/2018-05-trade.csv")
trade_df['hour'] = trade_df.apply(lambda x:pd.to_datetime(x['timestamp']).hour, axis=1)

all_arr = []
buy_arr = []
sell_arr = []

for i in range(0, 24):
    print(i)
    all_arr.append(len(trade_df[(trade_df['hour'] == i)]))
    buy_arr.append(len(trade_df[(trade_df['hour'] == i) & (trade_df['side'] == 0)]))
    sell_arr.append(len(trade_df[(trade_df['hour'] == i) & (trade_df['side'] == 1)]))

plot_df = pd.DataFrame([all_arr, sell_arr, buy_arr])
plot_df = plot_df.transpose()
plot_df.plot()

plt.title("Hourly Transaction Count")
plt.xlabel("timestamp_hour")
plt.ylabel("transaction_count")

graph = plt.legend()
graph.get_texts()[0].set_text('All')
graph.get_texts()[1].set_text('Buy')
graph.get_texts()[2].set_text('Sell')

plt.show()
