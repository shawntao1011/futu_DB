import logging
from queue import Queue


class TPPublisher:
    """
    Publish records to an im-memory queue.
    """

    def __init__(self, queue: Queue | None = None) -> None:
        self.queue = queue or Queue()
        self.logger = logging.getLogger(__name__)
