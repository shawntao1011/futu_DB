import logging
import os
import pykx as kx
from pykx import SyncQConnection

from src.publishers.tp_publisher import TPPublisher

class TorQPublisher(TPPublisher):
    """

    """
    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

