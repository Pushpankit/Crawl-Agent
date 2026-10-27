
# Simple Wake Agent

A lightweight, dependency-free Python script that periodically sends HTTP `GET` requests to one or more URLs. It can be used as a best-effort wake-up and availability-checking helper for hobby services, including Render web services.

The tool uses only Python's standard library. No third-party packages, `pip install`, or `requirements.txt` are required.

> **Important:** This tool does not guarantee that Render or any other hosting provider will keep a free service running. Hosting providers control their own suspension, restart, and resource policies. Periodic requests may help trigger an idle service, but they do not guarantee permanent uptime. For reliable, always-on availability, consider an appropriate paid hosting plan.

## Features

- **Dependency-free:** Uses Python's built-in libraries.
- **Multiple URLs:** Check one or several services in a single cycle.
- **Configurable interval:** Set how frequently requests are sent.
- **Configurable timeout:** Choose how long each request can wait for a response.
- **Request logging:** Displays timestamps, HTTP status codes, response times, and errors.
- **Error handling:** Continues running after individual request failures.
- **Graceful shutdown:** Stop the agent with `Ctrl+C`.
- **One-time check:** Run a single request cycle with the `--once` option.
- **Windows support:** Run it from PowerShell, the VS Code terminal, or a batch file.

## Requirements

- Python 3.9 or newer recommended.
- An internet connection.
- A publicly reachable HTTP or HTTPS URL.
- Permission to monitor the target service.

## Getting Started

### 1. Download the Project

Download `wake_agent.py` from this repository or clone the repository to your computer.

### 2. Open a Terminal

Open PowerShell or the integrated terminal in VS Code in the folder containing `wake_agent.py`.

### 3. Start the Agent

Replace the example URL with the URL of your own service.

```powershell
python wake_agent.py https://your-service.onrender.com
```

By default, the agent sends a request immediately and starts another check every 300 seconds (5 minutes).

Keep the terminal open while you want the agent to run.

To stop it, press `Ctrl+C`.

## Usage Examples

### Check a Service Every Five Minutes

```powershell
python wake_agent.py https://your-service.onrender.com
```

### Check Once and Exit

```powershell
python wake_agent.py https://your-service.onrender.com --once
```

### Configure the Interval and Timeout

Set the interval to five minutes and the request timeout to 60 seconds.

```powershell
python wake_agent.py https://your-service.onrender.com --interval 300 --timeout 60
```

### Check Multiple Services

```powershell
python wake_agent.py https://api.example.com/health https://another-service.onrender.com --interval 300
```

These commands assume that `wake_agent.py` supports the documented command-line options.

### Use a Health Endpoint

If your application provides a lightweight health endpoint, you can use it instead of the root URL.

```powershell
python wake_agent.py https://your-service.onrender.com/health
```

Only use a path that actually exists in your application. An HTTP `200 OK` response confirms that the requested URL responded successfully; it does not necessarily prove that every API route or database dependency is working correctly.

## Example Output

```text
Simple Wake Agent started
Targets: https://your-service.onrender.com
Interval: 300 seconds. Press Ctrl+C to stop.

[2026-10-27 19:00:00 IST] Check cycle started
[2026-10-27 19:00:01 IST] OK | HTTP 200 | 1.03s | https://your-service.onrender.com
[2026-10-27 19:00:01 IST] Cycle complete: 1/1 URLs returned HTTP 2xx/3xx
```

The actual output may vary depending on the implementation and configuration.

## Run Automatically on Windows

Create a file named `start-agent.bat` in the same folder as `wake_agent.py`.

Add the following content:

```bat
@echo off
cd /d "%~dp0"
python wake_agent.py https://your-service.onrender.com --interval 300
pause
```

Replace the example URL with your service URL.

Double-click `start-agent.bat` to start the agent.

For continued operation:

- Your computer must remain powered on and awake.
- Your internet connection must remain available.
- The Python process must continue running.

The agent will not run while your computer is shut down or asleep.

If the `python` command is not recognized, try replacing it with `py`:

```bat
@echo off
cd /d "%~dp0"
py wake_agent.py https://your-service.onrender.com --interval 300
pause
```

## Troubleshooting

### Python Is Not Recognized

Install Python and enable the option to add Python to your PATH during installation.

On Windows, you can also try:

```powershell
py wake_agent.py https://your-service.onrender.com
```

On macOS or Linux, try:

```bash
python3 wake_agent.py https://your-service.onrender.com
```

### HTTP 404 — Not Found

The server responded, but the requested path may not exist. Check the URL and endpoint.

### HTTP 401 or 403 — Unauthorized or Forbidden

The endpoint may require authentication or may deny the request. Use an endpoint you are authorized to access.

### HTTP 5xx — Server Error

The server returned an error. Check the hosting provider's logs and application health.

### Timeout or Connection Error

Check the URL, internet connection, DNS, TLS configuration, and whether the service is still starting.

### The Page Still Loads Slowly

Make sure you are checking the backend or API used by your frontend, rather than a separate frontend URL. The first request can still take time while a service starts.

### `KeyboardInterrupt`

This normally appears when you press `Ctrl+C` to stop the script. It is expected behavior, not necessarily an error.

## Limitations

Simple Wake Agent is a lightweight polling utility, not a full uptime-monitoring platform.

- It does not guarantee that a service will remain active.
- It cannot prevent a hosting provider from restarting or suspending a service.
- It does not provide alerts, a hosted scheduler, or guaranteed background execution.
- It depends on the computer running the script and having internet access.
- It does not guarantee that the application or its dependencies are healthy simply because a URL responds.
- Frequent requests may consume resources and are not recommended.

Render's free-service behavior and policies may change. Review the provider's current documentation before relying on any particular behavior.

## Responsible Use

Use reasonable polling intervals and only monitor services you own or have permission to check. Avoid excessive requests and follow your hosting provider's terms and usage policies.

For production-critical services, use appropriate hosting and monitoring solutions rather than relying on a locally running script.

## Contributing

Bug reports and focused improvements are welcome.

When reporting an issue, include:

- Python version.
- Operating system.
- Command used to run the script.
- Relevant error messages or logs.

Remove private URLs, credentials, tokens, and other sensitive information before sharing logs.

## Further Reading

- [Render: Deploy for Free](https://render.com/docs/free)
- [Render FAQ](https://render.com/docs/faq)
- [Python Documentation](https://docs.python.org/3/)
