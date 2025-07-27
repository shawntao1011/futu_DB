import logging
import os
import pykx as kx


logger = logging.getLogger(__name__)

class ArchivePublisher:
    """
    本地归档 Publisher：
      - 接收 table 名和 pykx.Table
      - 把它转换成 pandas.DataFrame
      - 按 table/时间戳写成 csv
    不做真正的 IPC 推送，只负责存盘。
    """

    def __init__(self, out_dir: str):
        self.out_dir = out_dir
        os.makedirs(self.out_dir, exist_ok=True)

    def publish(self, table: str, data: kx.Table):

        try:
            df = data.pd()
        except Exception as e:
            logger.error("transform back to dataframe failed: %s", e)

        file_path = os.path.join(self.out_dir, f"{table}.csv")

        write_header = not os.path.exists(file_path)
        df.to_csv(file_path, mode='a', index=False, header=write_header, encoding='utf-8-sig')

        print(f"[CSVArchivePublisher] Appended {len(df)} rows to {file_path}")
