# Simple Wake Agent

A small, dependency-free Python script that sends an HTTP `GET` request to one or more URLs on a schedule. It can be used as a best-effort wake-up/checking helper for hobby services, including Render web services.

**No third-party Python packages are required.** The script uses only the Python standard library.

> **Important:** This tool does not guarantee that Render or any other hosting provider will keep a free service running. Providers can restart or suspend services, and their plans and policies can change. Render documents that free web services spin down after 15 minutes without inbound traffic and take time to start on the next request. For dependable always-on availability, use an appropriate paid plan. Do not rely on this tool for production-critical services.

## Features

- One Python file; no `pip install` or `requirements.txt` needed.
- Checks one or several URLs.
- Configurable interval and request timeout.
- Prints timestamp, HTTP status, request duration, and errors.
- Continues after request failures.
- Handles `Ctrl+C` cleanly.
- Optional one-time check with `--once`.

## Requirements

- Python 3.9 or newer recommended.
- Internet access.
- The target URL must be publicly reachable over HTTP or HTTPS.

## Quick start

### Windows (PowerShell or VS Code terminal)

1. Download `wake_agent.py` from this repository, or clone the repository.
2. Open a terminal in the folder containing the file.
3. Run this command, replacing the URL with your service URL:

```powershell
python wake_agent.py https://your-service.onrender.com
```

By default, the script sends a request immediately and starts another check every **300 seconds (5 minutes)**. Keep the terminal open while you want it to run.

### macOS / Linux

```bash
python3 wake_agent.py https://your-service.onrender.com
```

## Examples

Check once and exit:

```bash
python wake_agent.py https://your-service.onrender.com --once
```

Check every five minutes with a 60-second request timeout:

```bash
python wake_agent.py https://your-service.onrender.com --interval 300 --timeout 60
```

Check multiple services in each cycle:

```bash
python wake_agent.py https://api.example.com/health https://another-service.onrender.com --interval 300
```

If your application has a lightweight health endpoint, prefer that URL, for example `https://your-service.onrender.com/health`. Only use a path that actually exists in your application. A root URL returning `200 OK` does not prove that every API route or database dependency is ready.

## Example output

```text
Simple Wake Agent started
Targets: https://your-service.onrender.com
Interval: 300 seconds. Press Ctrl+C to stop.
[2026-10-27 19:00:00 IST] Check cycle started
[2026-10-27 19:00:01 IST] OK | HTTP 200 | 1.03s | https://your-service.onrender.com
[2026-10-27 19:00:01 IST] Cycle complete: 1/1 URLs returned HTTP 2xx/3xx
```

## Run it automatically on Windows

You can create a file named `start-agent.bat` in the same folder:

```bat
@echo off
cd /d "%~dp0"
python wake_agent.py https://your-service.onrender.com --interval 300
pause
```

Replace the example URL. Double-click the `.bat` file to start the agent. The computer must remain awake, connected to the internet, and the process must remain running. This does not run when the laptop is shut down or asleep.

## Troubleshooting

- **`python` is not recognized:** install Python and enable “Add Python to PATH”, or try `py` on Windows / `python3` on macOS and Linux.
- **HTTP 404:** the server responded, but that URL path may not exist.
- **HTTP 401/403:** the endpoint requires authorization or denies the request.
- **HTTP 5xx:** the server returned an error; inspect the service logs.
- **Timeout or connection error:** check the URL, network, DNS, TLS, and whether the service is starting.
- **The page still loads slowly:** ensure you are checking the actual backend/API used by the frontend, not only a separate frontend URL. The first request can still be slow during a cold start.
- **`KeyboardInterrupt`:** this normally means you pressed `Ctrl+C` to stop the script; it is not a server error.

## Responsible use

Use reasonable intervals and only check services you own or have permission to monitor. This is a simple polling script, not a full uptime-monitoring system. It does not provide alerts, durable background execution, or a guarantee against cold starts. Very frequent requests are not recommended.

## Contributing

Bug reports and focused improvements are welcome. Please explain how to reproduce a bug and include Python version, operating system, command used, and relevant logs. Remove private URLs, tokens, and other secrets before posting logs.

## License

MIT. See [`LICENSE`](LICENSE).

## Further reading

- [Render: Deploy for Free](https://render.com/docs/free)
- [Render FAQ](https://render.com/docs/faq)
