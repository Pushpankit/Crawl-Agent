#!/usr/bin/env python3
"""Periodically send HTTP GET requests to one or more URLs.

Uses only the Python standard library. This is a lightweight availability
checker and best-effort wake-up helper; it cannot guarantee that a hosting
provider keeps a free service running.
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

USER_AGENT = "Simple-Wake-Agent/1.0 (+https://github.com/)"


def timestamp() -> str:
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def validate_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def check_url(url: str, timeout: float) -> bool:
    """GET a URL and log the status. Return True for 2xx/3xx responses."""
    request = Request(
        url,
        headers={"User-Agent": USER_AGENT, "Accept": "*/*"},
        method="GET",
    )
    started = time.monotonic()

    try:
        with urlopen(request, timeout=timeout) as response:
            status = response.status
            # Read a small amount so the response connection is cleanly handled.
            response.read(1024)
        elapsed = time.monotonic() - started
        ok = 200 <= status < 400
        label = "OK" if ok else "UNHEALTHY"
        print(f"[{timestamp()}] {label} | HTTP {status} | {elapsed:.2f}s | {url}", flush=True)
        return ok
    except HTTPError as exc:
        elapsed = time.monotonic() - started
        print(
            f"[{timestamp()}] HTTP ERROR | HTTP {exc.code} | {elapsed:.2f}s | {url}",
            flush=True,
        )
        return False
    except (URLError, TimeoutError, OSError) as exc:
        elapsed = time.monotonic() - started
        reason = getattr(exc, "reason", exc)
        print(
            f"[{timestamp()}] REQUEST FAILED | {reason} | {elapsed:.2f}s | {url}",
            flush=True,
        )
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Send periodic HTTP GET requests to one or more URLs."
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more complete URLs, e.g. https://your-service.onrender.com/health",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        metavar="SECONDS",
        help="Seconds between check cycles (default: 300 / 5 minutes; minimum: 60).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30,
        metavar="SECONDS",
        help="Timeout for each request (default: 30 seconds).",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run one check cycle and exit instead of repeating.",
    )
    args = parser.parse_args()

    invalid = [url for url in args.urls if not validate_url(url)]
    if invalid:
        parser.error("invalid URL(s): " + ", ".join(invalid))
    if args.interval < 60:
        parser.error("--interval must be at least 60 seconds")
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    return args


def main() -> int:
    args = parse_args()
    print("Simple Wake Agent started", flush=True)
    print(f"Targets: {', '.join(args.urls)}", flush=True)
    if args.once:
        print("Mode: one check cycle", flush=True)
    else:
        print(f"Interval: {args.interval} seconds. Press Ctrl+C to stop.", flush=True)

    try:
        while True:
            cycle_start = time.monotonic()
            print(f"[{timestamp()}] Check cycle started", flush=True)
            results = [check_url(url, args.timeout) for url in args.urls]
            print(
                f"[{timestamp()}] Cycle complete: {sum(results)}/{len(results)} URLs returned HTTP 2xx/3xx",
                flush=True,
            )
            if args.once:
                return 0 if all(results) else 1

            # Keep the cycle cadence approximately aligned to its start time.
            remaining = args.interval - (time.monotonic() - cycle_start)
            if remaining > 0:
                time.sleep(remaining)
    except KeyboardInterrupt:
        print(f"\n[{timestamp()}] Stopped by user.", flush=True)
        return 130


if __name__ == "__main__":
    sys.exit(main())
