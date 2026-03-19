from __future__ import annotations

from typing import Any

from ashare_strategy.data.providers.router import build_data_provider


def build_provider_diagnostics(config) -> dict[str, Any]:
    provider = build_data_provider(config)
    if not hasattr(provider, 'health_check'):
        return {
            'provider': config.data_source.provider,
            'status': 'unsupported',
            'message': '当前数据源暂不支持健康检查',
            'checks': [],
        }
    return provider.health_check().to_dict()


def format_provider_hint(diag: dict[str, Any]) -> str:
    status = diag.get('status', 'unknown')
    provider = diag.get('provider', '-')
    sdk = diag.get('sdk')
    prefix = f"数据源 {provider}" + (f"/{sdk}" if sdk else '')
    if status == 'ok':
        return f"{prefix} 当前健康，核心接口可用。"
    if status == 'degraded':
        return f"{prefix} 当前已降级到缓存模式，可先继续使用缓存数据。"
    if status == 'permission_limited':
        return f"{prefix} 已认证成功，但部分接口权限不足。"
    if status == 'auth_error':
        return f"{prefix} 认证失败，请检查 token/授权码。"
    if status == 'error':
        return f"{prefix} 当前不可用，请检查网络，或先执行 doctor-data 进一步诊断。"
    return f"{prefix} 当前状态：{status}。"
