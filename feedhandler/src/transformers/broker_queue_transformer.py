import pandas as pd


class BrokerQueueTransformer:


    def flattern(self, data: tuple[pd.DataFrame, pd.DataFrame]):

        bid_df = data[0].copy()
        ask_df = data[1].copy()

        if not bid_df.empty:
            bid_df = bid_df.rename(columns={
                'code': 'code',
                'name': 'name',
                'bid_broker_id': 'broker_id',
                'bid_broker_name': 'broker_name',
                'bid_broker_pos': 'broker_pos',
                'order_id': 'order_id',
                'order_volume': 'order_volume',
            })
            bid_df['side'] = 'bid'
            bid_df['time'] = pd.Timestamp.now()
            # bid_df 中的 order_id 和 order_volume 可能为None，甚至全部为None 无法被自动解析为Nan
            bid_df["order_id"] = pd.to_numeric(bid_df["order_id"], errors="coerce")
            bid_df["order_id"] = bid_df["order_id"].astype("Int64")
            bid_df["order_volume"] = pd.to_numeric(bid_df["order_volume"], errors="coerce")

        if not ask_df.empty:
            ask_df = ask_df.rename(columns={
                'code': 'code',
                'name': 'name',
                'ask_broker_id': 'broker_id',
                'ask_broker_name': 'broker_name',
                'ask_broker_pos': 'broker_pos',
                'order_id': 'order_id',
                'order_volume': 'order_volume',
            })
            ask_df['side'] = 'ask'
            ask_df['time'] = pd.Timestamp.now()
            # ask_df 中的 order_id 和 order_volume 可能为None，甚至全部为None 无法被自动解析为Nan
            ask_df["order_id"] = pd.to_numeric(ask_df["order_id"], errors="coerce")
            ask_df["order_id"] = ask_df["order_id"].astype("Int64")
            ask_df["order_volume"] = pd.to_numeric(ask_df["order_volume"], errors="coerce")

        out_df = pd.concat(
            [bid_df, ask_df], ignore_index=True
        )

        return out_df
