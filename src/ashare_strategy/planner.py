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
        positions = self.service.load_positions()
        current_codes = {p.get('stock_code') for p in positions}
        buy_candidates = candidates[~candidates['stock_code'].isin(current_codes)] if not candidates.empty else pd.DataFrame()
        hold_list = [p for p in positions if p.get('stock_code') in current_codes]
        suggested_sells = []
        for p in positions:
            suggested_sells.append({
                'stock_code': p.get('stock_code'),
                'stock_name': p.get('stock_name', ''),
                'reason': '需结合最新行情检查是否跌破5日线/首阳开盘价或达到持有天数',
            })
        summary = {
            'plan_date': datetime.utcnow().strftime('%Y-%m-%d'),
            'candidate_count': int(len(candidates)) if not candidates.empty else 0,
            'buy_count': int(len(buy_candidates)) if not buy_candidates.empty else 0,
            'hold_count': len(hold_list),
            'sell_review_count': len(suggested_sells),
        }
        return {
            'summary': summary,
            'buy_candidates': buy_candidates.to_dict(orient='records') if not buy_candidates.empty else [],
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
