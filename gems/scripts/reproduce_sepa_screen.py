#!/usr/bin/env python3
"""Reproduce the price-only SEPA pre-screen from Yahoo Chart API data."""

import datetime as dt
import hashlib
import json
from statistics import fmean
from urllib.parse import quote
from urllib.request import Request, urlopen

TICKERS = ["VRT", "FIX", "CLS", "COHR", "CRDO", "POWL", "CIEN"]
START = dt.datetime(2025, 7, 1, tzinfo=dt.timezone.utc)
END = dt.datetime(2026, 8, 1, tzinfo=dt.timezone.utc)


def fetch(symbol: str) -> list[tuple[int, float]]:
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{quote(symbol)}"
        f"?period1={int(START.timestamp())}&period2={int(END.timestamp())}"
        "&interval=1d&events=history&includeAdjustedClose=true"
    )
    request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
    data = json.loads(urlopen(request, timeout=30).read())["chart"]["result"][0]
    values = data["indicators"]["adjclose"][0]["adjclose"]
    return [(stamp, float(value)) for stamp, value in zip(data["timestamp"], values) if value is not None]


def summarize(symbol: str) -> dict[str, object]:
    pairs = fetch(symbol)
    values = [value for _, value in pairs]
    assert len(values) == 273
    compact = json.dumps(pairs, separators=(",", ":"))
    return {
        "ticker": symbol,
        "n": len(values),
        "P": values[-1],
        "MA50": fmean(values[-50:]),
        "MA150": fmean(values[-150:]),
        "MA200": fmean(values[-200:]),
        "L252": min(values[-252:]),
        "H252": max(values[-252:]),
        "sha256": hashlib.sha256(compact.encode()).hexdigest(),
    }


if __name__ == "__main__":
    print(json.dumps([summarize(ticker) for ticker in TICKERS], indent=2))
