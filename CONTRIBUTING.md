# Contributing

1. Open an issue describing the bug or proposed change before major changes.
2. Keep the project dependency-free unless a dependency is clearly justified.
3. Test the script with `--once` against a URL you own or are authorized to check.
4. Do not commit credentials, private URLs, or personal data in logs.
5. Keep documentation accurate about hosting-provider limitations; do not promise that polling can guarantee an always-on free service.

## Local test

```bash
python wake_agent.py https://example.com --once
```
