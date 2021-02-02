# Run on Metro M4 Airlift w RGB Matrix shield and 64x32 matrix display
# show current value of Bitcoin in USD

import time
import board
import terminalio
from adafruit_matrixportal.matrixportal import MatrixPortal

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# You can display in 'GBP', 'EUR' or 'USD'
CURRENCY = "USD"
STOCK = "GME"
APIKEY = secrets["stonks_key"]
# Set up where we'll be fetching data from
DATA_SOURCE = "https://finnhub.io/api/v1/quote?symbol="+ STOCK +"&token="+ APIKEY
DATA_LOCATION = ["c"]


def text_transform(val):
    if CURRENCY == "USD":
        return "$%d" % val
    if CURRENCY == "EUR":
        return "‎€%d" % val
    if CURRENCY == "GBP":
        return "£%d" % val
    return "%d" % val


# the current working directory (where this file is)
cwd = ("/" + __file__).rsplit("/", 1)[0]

matrixportal = MatrixPortal(
    url=DATA_SOURCE,
    json_path=DATA_LOCATION,
    status_neopixel=board.NEOPIXEL,
    default_bg=cwd + "/GME_background.bmp",
    debug=True,
)

matrixportal.add_text(
    text_font=terminalio.FONT,
    text_position=(19, 19),
    text_color=0x3d1f5c,
    text_transform=text_transform,
)
matrixportal.preload_font(b"$012345789")  # preload numbers
matrixportal.preload_font((0x00A3, 0x20AC))  # preload gbp/euro symbol

while True:
    try:
        value = matrixportal.fetch()
        print("Response is", value)
    except (ValueError, RuntimeError) as e:
        print("Some error occured, retrying! -", e)

    time.sleep(15 * 60)  # wait 15 minutes
