import time
from datetime import datetime
from . import config
from .data_sources import polygon_top_by_market_cap
from .utils import log

class Top500Cache:
    def __init__(self):
        self.tickers: list[str] = []
        self.cap_map: dict[str, float] = {}
        self.last_refresh_date = None

    def needs_refresh(self) -> bool:
        return self.last_refresh_date != datetime.now(config.ET).date()

    def refresh_now(self):
        log("Refreshing Top-500 (S&P constituents)…")
        t0 = time.time()
        self.tickers, self.cap_map = polygon_top_by_market_cap(500)
        self.last_refresh_date = datetime.now(config.ET).date()
        log(f"Refresh complete in {time.time()-t0:.1f}s. Loaded {len(self.tickers)} symbols.")
