import random
from datetime import datetime, timezone
from .utils import log, send_email
from .markets import submit_notional_buy
from .stream import JellyStream
from .cache import Top500Cache

def hourly_cycle(tc, stream: JellyStream, cache: Top500Cache):
    log("Hourly cycle starting…")

    if not cache.tickers:
        cache.refresh_now()

    ten = random.sample(cache.tickers, k=min(10, len(cache.tickers)))
    ten_sorted = sorted(ten, key=lambda s: cache.cap_map.get(s, 0.0), reverse=True)
    log("Chosen 10 (cap-desc):", ten_sorted)

    count = stream.snapshot_count()
    log(f"Jellyfish snapshot count = {count}")

    if count <= 0:
        pick = ten_sorted[0]
        log("Count = 0 → fallback to first stock:", pick)
    elif count > len(ten_sorted):
        pick = ten_sorted[-1]
        log(f"Count > {len(ten_sorted)} → fallback to last stock:", pick)
    else:
        pick = ten_sorted[count - 1]
        log(f"Picked #{count} -> {pick}")

    notional = max(1.0, float(count))
    try:
        order = submit_notional_buy(tc, pick, notional)
        log("Submitted paper order:", order)
        send_email(
            subject=f"Jellyfish Trade: Bought ${notional:.2f} of {pick}",
            body=(f"UTC: {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}\n"
                  f"Jellyfish count: {count}\n"
                  f"Picked {pick} from: {ten_sorted}\n"
                  f"Amount: ${notional:.2f}\n"
                  f"Market Cap: {cache.cap_map.get(pick)}\n"),
        )
    except Exception as e:
        log("Order submission failed:", e)
