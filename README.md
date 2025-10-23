# Jellyfish Trading Bot With Alpaca API

- Captures a frame each hour while the market is open (per Alpaca clock).
- Uses HSV masking to track the movement of jellyfish via the Georgia Aquarium livestream.
- Picks a stock based off the OpenCV output and submits a paper notional buy with Alpaca's API.
- Refreshes tickers daily.
- Serves health endpoints for deployment checks.

Environment variables (minimum):
```bash
export ALPACA_API_KEY=...
export ALPACA_API_SECRET=...
export LINK="rtsp/http stream url"
# optional email notifications
export SMTP_HOST=...
export SMTP_PORT=587
export SMTP_USERNAME=...
export SMTP_PASSWORD=...
export EMAIL_FROM=you@example.com
export EMAIL_TO=you@example.com
```

## HTTP endpoints
- `GET /` – root info
- `GET /health` – health check

## Project layout
```
  config.py        # knobs & env
  utils.py         # logging, email
  vision.py        # HSV mask + counting
  data_sources.py  # S&P-500 fetch
  markets.py       # Alpaca helpers
  stream.py        # video capture
  schedule.py      # timing helpers
  cache.py         # daily ticker cache
  cycle.py         # one trading cycle
  server.py        # Flask app
  main.py          # orchestration/entry
requirements.txt
```

## Notes
- Uses Alpaca paper trading by default.
- Tune HSV thresholds in `config.py`.
- Requires OpenCV build with FFMPEG support.
