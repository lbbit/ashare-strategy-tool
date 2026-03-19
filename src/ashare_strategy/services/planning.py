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
        account = self.portfolio_service.load_account()
        cash = float(account.get('cash') or 0.0)
        total_asset = float(account.get('total_asset') or cash)
        current_codes = {p.get('stock_code') for p in positions}
        buy_candidates = candidates[~candidates['stock_code'].isin(current_codes)] if not candidates.empty else candidates
        hold_list = [p for p in positions if p.get('stock_code') in current_codes]
        slots_left = max(self.config.max_positions - len(hold_list), 0)
        planned_buy_count = min(int(len(buy_candidates)) if not buy_candidates.empty else 0, slots_left, self.config.max_daily_buys)
        planned_buy_budget = cash / planned_buy_count if planned_buy_count > 0 else 0.0
        suggested_buys = []
        if planned_buy_count > 0 and not buy_candidates.empty:
            for row in buy_candidates.head(planned_buy_count).to_dict(orient='records'):
                row['suggested_budget'] = round(planned_buy_budget, 2)
                suggested_buys.append(row)
        suggested_sells = [
            {
                'stock_code': p.get('stock_code'),
                'stock_name': p.get('stock_name', ''),
                'shares': p.get('shares', 0),
                'available_shares': p.get('available_shares', p.get('shares', 0)),
                'latest_price': p.get('latest_price'),
                'reason': '需结合最新行情检查是否跌破5日线/首阳开盘价或达到持有天数',
            }
            for p in positions
        ]
        from datetime import datetime
        return {
            'summary': {
                'plan_date': datetime.utcnow().strftime('%Y-%m-%d'),
                'candidate_count': int(len(candidates)) if not candidates.empty else 0,
                'buy_count': len(suggested_buys),
                'hold_count': len(hold_list),
                'sell_review_count': len(suggested_sells),
                'cash': cash,
                'total_asset': total_asset,
                'market_value': float(account.get('market_value') or 0.0),
                'slots_left': slots_left,
            },
            'buy_candidates': suggested_buys,
            'hold_positions': hold_list,
            'sell_review': suggested_sells,
        }
