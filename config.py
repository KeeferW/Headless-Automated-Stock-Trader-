import os
from zoneinfo import ZoneInfo

# Stream
STREAM_URL = os.environ.get("LINK", "")

# Mask / detection knobs
MASK_LOWER = (20, 100, 130)   # Lower HSV
MASK_UPPER = (130, 255, 255)  # Upper HSV
OPEN_ITERS = 1
CLOSE_ITERS = 1
MIN_AREA = 500
COUNT_GRACE_FRAMES = 10

# Alpaca
ALPACA_API_KEY = os.environ.get("ALPACA_API_KEY", "")
ALPACA_API_SECRET = os.environ.get("ALPACA_API_SECRET", "")
ALPACA_BASE_URL = os.environ.get("ALPACA_BASE_URL", "https://paper-api.alpaca.markets")

# Email
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USERNAME = os.environ.get("SMTP_USERNAME", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
EMAIL_FROM = os.environ.get("EMAIL_FROM", "")
EMAIL_TO = os.environ.get("EMAIL_TO", "")

# Timezone
ET = ZoneInfo("America/New_York")
