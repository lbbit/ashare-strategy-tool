from __future__ import annotations

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.planner import TradingPlanner
from ashare_strategy.services.portfolio import PortfolioService
from ashare_strategy.services.screening import ScreeningService


class PlanningService:
    def __init__(self, screening_service: ScreeningService, portfolio_service: PortfolioService, config: StrategyConfig) -> None:
        self.planner = TradingPlannerAdapter(screening_service, portfolio_service, config)

    def export_daily_plan(self, output_dir: str = 'daily_plan'):
        return self.planner.export_daily_plan(output_dir)


class TradingPlannerAdapter(TradingPlanner):
    def __init__(self, screening_service: ScreeningService, portfolio_service: PortfolioService, config: StrategyConfig) -> None:
        self.screening_service = screening_service
        self.portfolio_service = portfolio_service
        self.config = config

    def build_daily_plan(self) -> dict:
        candidates = self.screening_service.run()
        positions = self.portfolio_service.load_positions()
        current_codes = {p.get('stock_code') for p in positions}
        buy_candidates = candidates[~candidates['stock_code'].isin(current_codes)] if not candidates.empty else candidates
        hold_list = [p for p in positions if p.get('stock_code') in current_codes]
        suggested_sells = [
            {
                'stock_code': p.get('stock_code'),
                'stock_name': p.get('stock_name', ''),
                'reason': '需结合最新行情检查是否跌破5日线/首阳开盘价或达到持有天数',
            }
            for p in positions
        ]
        from datetime import datetime
        return {
            'summary': {
                'plan_date': datetime.utcnow().strftime('%Y-%m-%d'),
                'candidate_count': int(len(candidates)) if not candidates.empty else 0,
                'buy_count': int(len(buy_candidates)) if not buy_candidates.empty else 0,
                'hold_count': len(hold_list),
                'sell_review_count': len(suggested_sells),
            },
            'buy_candidates': buy_candidates.to_dict(orient='records') if not buy_candidates.empty else [],
            'hold_positions': hold_list,
            'sell_review': suggested_sells,
        }
