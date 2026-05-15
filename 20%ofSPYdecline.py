import yfinance as yf
from datetime import date
import subprocess

ticker = "^GSPC"

data = yf.Ticker(ticker).history(period="max")

ath = data["High"].max()

latest = data.iloc[-1]
latest_date = data.index[-1].date()
latest_high = latest["High"]
latest_low = latest["Low"]

drawdown = (latest_low - ath) / ath * 100

today = date.today()

print(f"=== {today} S&P 500 ATH下落率チェック ===")
print(f"最新取引日: {latest_date}")
print(f"S&P 500 ATH: {ath:.2f}")
print(f"最新高値: {latest_high:.2f}")
print(f"最新安値: {latest_low:.2f}")
print(f"ATHから最新安値までの下落率: {drawdown:.2f}%")

if drawdown <= -20:
    alert_message = (
        f"S&P 500 is down {drawdown:.2f}% from ATH.\n\n"
        "今すぐ積立投資を完全にレバナスへ切り替えてください。"
    )

elif drawdown <= -10:
    alert_message = (
        f"S&P 500 is down {drawdown:.2f}% from ATH.\n\n"
        "今すぐ積立投資の半分、25万円をレバナスへ切り替えてください。"
    )

elif drawdown < 0:
    alert_message = (
        f"S&P 500 is down {drawdown:.2f}% from ATH.\n\n"
        "下落トレンド入りかもしれません。\n"
        "来たるべき時のために、レバナスの準備をしてください。"
    )

else:
    alert_message = (
        f"S&P 500 is {drawdown:.2f}% from ATH.\n\n"
        "相場は調子が良いみたいですね。\n"
        "積立額がどんどん膨らんでいます。"
    )

import requests

requests.post(
    "https://ntfy.sh/SP500_ALERT",
    data=alert_message.encode("utf-8"),
    headers={
        "Title": "S&P 500 Alert",
        "Priority": "high",
        "Tags": "chart_with_downwards_trend"
    }
)