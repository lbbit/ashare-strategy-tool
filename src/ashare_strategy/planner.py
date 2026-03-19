from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.execution.portfolio import TradingService


class TradingPlanner:
    def __init__(self, service: TradingService, config: StrategyConfig) -> None:
        self.service = service
        self.config = config

    def build_daily_plan(self) -> dict:
        candidates = self.service.screen()
        account = self.service.load_account() if hasattr(self.service, 'load_account') else {'cash': 0.0, 'positions': self.service.load_positions()}
        positions = account.get('positions', [])
        current_codes = {p.get('stock_code') for p in positions}
        buy_candidates = candidates[~candidates['stock_code'].isin(current_codes)] if not candidates.empty else pd.DataFrame()
        hold_list = [p for p in positions if p.get('stock_code') in current_codes]
        cash = float(account.get('cash') or 0.0)
        slots_left = max(self.config.max_positions - len(hold_list), 0)
        planned_buy_count = min(int(len(buy_candidates)) if not buy_candidates.empty else 0, slots_left, self.config.max_daily_buys)
        per_trade_budget = cash / planned_buy_count if planned_buy_count > 0 else 0.0
        buy_list = []
        if planned_buy_count > 0 and not buy_candidates.empty:
            for row in buy_candidates.head(planned_buy_count).to_dict(orient='records'):
                row['suggested_budget'] = round(per_trade_budget, 2)
                buy_list.append(row)
        suggested_sells = []
        for p in positions:
            suggested_sells.append({
                'stock_code': p.get('stock_code'),
                'stock_name': p.get('stock_name', ''),
                'shares': p.get('shares', 0),
                'available_shares': p.get('available_shares', p.get('shares', 0)),
                'latest_price': p.get('latest_price'),
                'reason': '需结合最新行情检查是否跌破5日线/首阳开盘价或达到持有天数',
            })
        summary = {
            'plan_date': datetime.utcnow().strftime('%Y-%m-%d'),
            'candidate_count': int(len(candidates)) if not candidates.empty else 0,
            'buy_count': len(buy_list),
            'hold_count': len(hold_list),
            'sell_review_count': len(suggested_sells),
            'cash': cash,
            'total_asset': float(account.get('total_asset') or 0.0),
            'market_value': float(account.get('market_value') or 0.0),
            'slots_left': slots_left,
        }
        return {
            'summary': summary,
            'buy_candidates': buy_list,
            'hold_positions': hold_list,
            'sell_review': suggested_sells,
        }

    def export_daily_plan(self, output_dir: str = 'daily_plan') -> dict:
        plan = self.build_daily_plan()
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        pd.DataFrame([plan['summary']]).to_csv(out / 'summary.csv', index=False)
        pd.DataFrame(plan['buy_candidates']).to_csv(out / 'buy_candidates.csv', index=False)
        pd.DataFrame(plan['hold_positions']).to_csv(out / 'hold_positions.csv', index=False)
        pd.DataFrame(plan['sell_review']).to_csv(out / 'sell_review.csv', index=False)
        return {'output_dir': str(out), 'plan': plan}
