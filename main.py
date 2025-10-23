import threading
import time
from datetime import datetime, timedelta, timezone

from . import config
from .utils import log
from .markets import alpaca_clock, alpaca_trading_client
from .stream import JellyStream
from .cache import Top500Cache
from .cycle import hourly_cycle
from .schedule import (
    wait_until,
    top_of_next_hour_utc,
    next_855am_et_after,
    is_weekday_et,
)
from .server import run_flask_server

def run_bot():
    if not (config.ALPACA_API_KEY and config.ALPACA_API_SECRET):
        raise SystemExit("Set ALPACA_API_KEY and ALPACA_API_SECRET as secrets.")

    tc = alpaca_trading_client()
    stream = JellyStream(config.STREAM_URL)
    cache = Top500Cache()
    next_refresh_utc = next_855am_et_after(datetime.now(timezone.utc))

    while True:
        now_utc = datetime.now(timezone.utc)
        if now_utc >= next_refresh_utc and is_weekday_et(now_utc):
            if cache.needs_refresh():
                try:
                    cache.refresh_now()
                except Exception as e:
                    log("Daily refresh failed:", e)
            next_refresh_utc = next_855am_et_after(now_utc + timedelta(seconds=1))

        try:
            clk = alpaca_clock()
            if not getattr(clk, "is_open", False):
                next_open = getattr(clk, "next_open", None)
                log("Market closed. Waiting until", next_open)
                wake = min(next_open, next_refresh_utc) if (next_open and is_weekday_et(now_utc)) else (next_open or next_refresh_utc)
                wait_until(wake)
                continue
        except Exception as e:
            log("Clock check failed, sleeping 30 min:", e)
            time.sleep(1800)
            continue

        log("Market OPEN — opening stream")
        stream.open()
        log("Stream opened, hourly cycle starting")
        hourly_cycle(tc, stream, cache)
        log("Hourly cycle complete, closing stream")

        while True:
            try:
                if not alpaca_clock().is_open:  # type: ignore
                    log("Market CLOSED — closing stream")
                    stream.close()
                    break
            except Exception:
                pass

            nxt = top_of_next_hour_utc()
            wait_until(min(nxt, next_refresh_utc))

            now_utc = datetime.now(timezone.utc)
            if now_utc >= next_refresh_utc and is_weekday_et(now_utc) and cache.needs_refresh():
                try:
                    cache.refresh_now()
                except Exception as e:
                    log("Daily refresh (in-session) failed:", e)
                next_refresh_utc = next_855am_et_after(now_utc + timedelta(seconds=1))

            try:
                if alpaca_clock().is_open:  # type: ignore
                    hourly_cycle(tc, stream, cache)
            except Exception:
                hourly_cycle(tc, stream, cache)

        time.sleep(10)

def main():
    log("Jelly Bot starting…")
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    run_bot()

if __name__ == "__main__":
    main()
