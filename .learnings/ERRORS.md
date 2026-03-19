## [ERR-20260318-001] environment_bootstrap_timeout

**Logged**: 2026-03-18T16:24:26Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Initial environment bootstrap timed out while creating venv and installing dependencies.

### Error
```
TimeoutError: The command execution exceeded the timeout of 120 seconds.
```

### Context
- Attempted to create Python virtualenv and install project dependencies in one shell command.
- The installation step exceeded the tool timeout.

### Suggested Fix
Split bootstrap into smaller steps and increase timeout for dependency installation.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md

---
## [ERR-20260318-002] brace_expansion_in_mkdir

**Logged**: 2026-03-18T16:24:50Z
**Priority**: low
**Status**: pending
**Area**: infra

### Summary
Using brace expansion with nested path segments did not create expected directories in this shell invocation.

### Error
```
touch: cannot touch 'src/ashare_strategy/data/__init__.py': No such file or directory
```

### Context
- Attempted: mkdir -p src/ashare_strategy/{data,strategies,...}
- Follow-up touch failed because directories were not created as expected.

### Suggested Fix
Create directories explicitly or verify shell brace expansion behavior before relying on it.

### Metadata
- Reproducible: yes
- Related Files: .learnings/ERRORS.md

---
## [ERR-20260318-003] pip_install_timeout

**Logged**: 2026-03-18T16:28:12Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Editable install with dependencies timed out during package resolution/download.

### Error
```
TimeoutError: The command execution exceeded the timeout of 240 seconds.
```

### Context
- Command: python3 -m pip install -e .[dev]
- Likely due to large dependency set and network speed.

### Suggested Fix
Install core dependencies incrementally or allow longer timeout in CI/bootstrap.

### Metadata
- Reproducible: unknown
- Related Files: pyproject.toml

---
## [ERR-20260318-004] test_import_requires_akshare

**Logged**: 2026-03-18T16:29:02Z
**Priority**: low
**Status**: pending
**Area**: tests

### Summary
Test collection failed because selector imports provider module which requires akshare.

### Error
```
ModuleNotFoundError: No module named 'akshare'
```

### Context
- Running minimal tests without full dependency installation.
- Tests should avoid importing heavy runtime dependencies when not needed.

### Suggested Fix
Make akshare an optional runtime import inside provider methods or install it before tests.

### Metadata
- Reproducible: yes
- Related Files: src/ashare_strategy/data/provider.py, tests/test_selector_logic.py

---
## [ERR-20260318-005] github_push_transport_auth

**Logged**: 2026-03-18T16:40:20Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
GitHub push initially failed due to missing HTTPS credential setup, then failed again due to HTTP2 transport error.

### Error
```
fatal: could not read Username for 'https://github.com': No such device or address
fatal: unable to access 'https://github.com/lbbit/ashare-strategy-tool.git/': Error in the HTTP2 framing layer
```

### Context
- Repo created successfully with gh.
- `gh auth setup-git` fixed credential helper issue.
- Network/transport still unstable for push.

### Suggested Fix
Retry with HTTP/1.1, SSH remote, or a later network retry.

### Metadata
- Reproducible: unknown
- Related Files: .learnings/ERRORS.md

---
## [ERR-20260319-006] live_backtest_network_dependency

**Logged**: 2026-03-19T00:54:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
CLI live backtest test failed because AkShare spot request was disconnected by remote endpoint.

### Error
```
ConnectionError: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
```

### Context
- Command: PYTHONPATH=src python3 -m ashare_strategy.cli backtest --mode rolling --export-report-dir reports_test
- Failure happened during `stock_zh_a_spot_em()` live request.

### Suggested Fix
Add graceful error handling and offline-friendly fallback messaging for live data fetch failures.

### Metadata
- Reproducible: unknown
- Related Files: src/ashare_strategy/data/provider.py, src/ashare_strategy/cli.py

---
