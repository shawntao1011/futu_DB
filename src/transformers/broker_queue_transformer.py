import pandas as pd


class BrokerQueueTransformer:


    def flattern(self, data: tuple[str, pd.DataFrame, pd.DataFrame]):

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

        out_df = pd.concat(
            [bid_df, ask_df], ignore_index=True
        )

        return out_df
