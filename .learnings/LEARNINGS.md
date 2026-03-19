## [LRN-20260318-001] best_practice

**Logged**: 2026-03-18T23:37:37Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
当前环境已存在可用于 GitHub SSH 推送的 `/root/.ssh/id_ed25519`，且用户已提前添加对应公钥，应优先使用 SSH remote 而不是 HTTPS。

### Details
用户明确说明曾为当前环境添加过公钥。检查确认 `/root/.ssh/id_ed25519.pub` 存在，公钥为 `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOizVbUBjeOsJfWTYwKCQJjcJZVEVdrR1CWDyDCEl9Vt ou_516544ee3139f1c48c9cf4c6136a7499@feishu`。因此 GitHub 仓库推送应优先切换为 SSH 协议，避免 HTTPS 凭证与网络层额外问题。

### Suggested Action
后续凡是 GitHub push/pull 场景，优先检查并复用现有 SSH key 与 SSH remote。

### Metadata
- Source: conversation
- Related Files: .learnings/LEARNINGS.md
- Tags: github, ssh, git

---
## [LRN-20260319-008] best_practice

**Logged**: 2026-03-19T02:10:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
Data provider layer should support reliable free-source fallback plus token-configured premium provider selection without breaking local persisted config.

### Details
User clarified long-term need: keep free source usable, but add Tushare Pro provider with configurable token persistence and avoid wasting quota during testing. This implies provider routing, credential storage in config, low-volume smoke tests, and reliability improvements such as retries/timeouts/cache fallback.

### Suggested Action
Implement provider config fields for auth, add Tushare provider with minimal endpoint usage, and harden AkShare provider with retries/timeouts/cache fallback semantics.

### Metadata
- Source: conversation
- Related Files: src/ashare_strategy/data/provider.py, src/ashare_strategy/core/config.py, config/default_strategy.yaml
- Tags: provider, reliability, tushare

---
## [LRN-20260319-009] correction

**Logged**: 2026-03-19T02:32:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
Previously treating the second credential as invalid for Tushare was incorrect because it is a Tinyshare authorization code, not a native Tushare token.

### Details
User clarified the purchased credential is for Tinyshare SDK compatibility, which requires `import tinyshare as ts` while preserving Tushare-style `pro_api()` calls. After switching SDK, low-volume smoke tests succeeded for `index_daily`, `daily`, and `trade_cal`.

### Suggested Action
Add Tinyshare-compatible provider option or allow Tushare provider to select SDK backend via config, and document credential type differences clearly.

### Metadata
- Source: user_feedback
- Related Files: src/ashare_strategy/data/providers/tushare.py, docs/USER_GUIDE.md, docs/DATA_PROVIDER_RESEARCH.md
- Tags: tinyshare, tushare, correction

---
