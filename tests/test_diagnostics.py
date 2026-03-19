from ashare_strategy.data.diagnostics import format_provider_hint


def test_format_provider_hint_auth_error():
    hint = format_provider_hint({'provider': 'tushare', 'sdk': 'tinyshare', 'status': 'auth_error'})
    assert '认证失败' in hint


def test_format_provider_hint_degraded():
    hint = format_provider_hint({'provider': 'akshare', 'status': 'degraded'})
    assert '缓存模式' in hint
