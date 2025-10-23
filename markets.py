from datetime import datetime, timezone
from . import config
from .utils import log

def alpaca_trading_client():
    from alpaca.trading.client import TradingClient
    return TradingClient(config.ALPACA_API_KEY, config.ALPACA_API_SECRET, paper=True)

def alpaca_clock():
    from alpaca.trading.client import TradingClient
    tc = TradingClient(config.ALPACA_API_KEY, config.ALPACA_API_SECRET, paper=True)
    return tc.get_clock()

def submit_notional_buy(tc, symbol: str, usd: float):
    from alpaca.trading.requests import MarketOrderRequest
    from alpaca.trading.enums import OrderSide, TimeInForce
    if usd <= 0:
        return None
    req = MarketOrderRequest(
        symbol=symbol,
        notional=round(float(usd), 2),
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
    )
    order = tc.submit_order(req)
    log(f"Order placed at {datetime.now(timezone.utc).isoformat()}: {symbol} ${usd:.2f}")
    return order
