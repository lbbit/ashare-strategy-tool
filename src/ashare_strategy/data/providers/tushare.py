from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

from ashare_strategy.data.cache import CsvCache
from ashare_strategy.data.health import ProviderHealthCheck


class TushareProvider:
    def __init__(self, token: str, cache_dir: str = '.cache/market_data', use_cache: bool = True, sdk: str = 'tushare') -> None:
        self.token = token
        self.cache = CsvCache(cache_dir, enabled=use_cache)
        self._pro = None
        self.sdk = sdk

    def _client(self):
        if self._pro is None:
            if self.sdk == 'tinyshare':
                import tinyshare as ts
            else:
                import tushare as ts
            ts.set_token(self.token)
            self._pro = ts.pro_api()
        return self._pro

    @staticmethod
    def _normalize_dates(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
        out = df.copy()
        out[date_col] = pd.to_datetime(out[date_col])
        return out.sort_values(date_col).reset_index(drop=True)

    def _safe_call(self, name: str, func):
        try:
            df = func()
            return {"name": name, "status": "ok", "rows": len(df)}
        except Exception as e:
            msg = str(e)
            status = 'auth_error' if 'token不对' in msg or 'token 不对' in msg else 'permission_error' if '没有接口访问权限' in msg else 'error'
            return {"name": name, "status": status, "message": msg}

    def health_check(self) -> ProviderHealthCheck:
        checks = [
            self._safe_call('trade_cal', lambda: self._client().trade_cal(exchange='SSE', start_date='20250301', end_date='20250305').head(3)),
            self._safe_call('daily', lambda: self._client().daily(ts_code='000001.SZ', start_date='20250301', end_date='20250305').head(3)),
            self._safe_call('index_daily', lambda: self._client().index_daily(ts_code='000300.SH', start_date='20250301', end_date='20250305').head(3)),
        ]
        auth_ok = any(item['status'] == 'ok' for item in checks)
        if auth_ok:
            status = 'ok'
            message = '至少一个核心接口可用'
        elif any(item['status'] == 'permission_error' for item in checks):
            status = 'permission_limited'
            message = '认证成功，但部分目标接口权限不足'
        elif any(item['status'] == 'auth_error' for item in checks):
            status = 'auth_error'
            message = 'token/授权码无效或已过期'
        else:
            status = 'error'
            message = '接口检查失败，请检查网络或服务状态'
        return ProviderHealthCheck(provider='tushare', sdk=self.sdk, status=status, auth_ok=auth_ok, cache_enabled=self.cache.enabled, checks=checks, message=message)

    def get_stock_daily(self, symbol: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
        start = (start_date or (datetime.today().date() - timedelta(days=365)).strftime('%Y%m%d')).replace('-', '')
        end = (end_date or datetime.today().date().strftime('%Y%m%d')).replace('-', '')
        ts_code = f"{symbol}.SZ" if symbol.startswith(('000', '001', '002', '003', '300')) else f"{symbol}.SH"
        df = self.cache.load_or_fetch(f'ts_stock_daily_{symbol}_{start}_{end}', lambda: self._client().daily(ts_code=ts_code, start_date=start, end_date=end))
        df = df.rename(columns={'trade_date': 'date', 'open': 'open', 'close': 'close', 'high': 'high', 'low': 'low', 'vol': 'volume', 'pct_chg': 'pct_chg'})
        return self._normalize_dates(df)

    def get_spot(self) -> pd.DataFrame:
        raise NotImplementedError('TushareProvider 暂未实现实时行情接口')

    def get_benchmark_daily(self, symbol: str = 'sh000300') -> pd.DataFrame:
        index_code = '000300.SH' if symbol == 'sh000300' else symbol
        try:
            df = self.cache.load_or_fetch(f'ts_benchmark_{index_code}', lambda: self._client().index_daily(ts_code=index_code))
        except Exception:
            return pd.DataFrame(columns=['date', 'open', 'close', 'high', 'low', 'volume'])
        df = df.rename(columns={'trade_date': 'date', 'open': 'open', 'close': 'close', 'high': 'high', 'low': 'low', 'vol': 'volume'})
        return self._normalize_dates(df)

    def get_board_names(self) -> pd.DataFrame:
        return pd.DataFrame(columns=['板块名称'])

    def get_board_hist(self, board_name: str) -> pd.DataFrame:
        return pd.DataFrame(columns=['date', 'open', 'close', 'high', 'low', 'volume'])

    def get_board_cons(self, board_name: str) -> pd.DataFrame:
        return pd.DataFrame(columns=['代码', '名称'])

    def get_recent_trade_range(self, days: int = 365) -> tuple[str, str]:
        end = datetime.today().date()
        start = end - timedelta(days=days * 2)
        return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')
