from __future__ import annotations

import pandas as pd
import streamlit as st

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.execution.portfolio import TradingService

st.set_page_config(page_title="A股策略工具", layout="wide")
st.title("A股选股与回测工具")

with st.sidebar:
    st.header("参数")
    board_min_volume = st.number_input("板块近5日最小成交量", value=120.0)
    stock_float_cap_max = st.number_input("流通A股上限", value=1_000_000_000.0)
    first_day_gain_pct = st.number_input("首日涨幅阈值(%)", value=7.0)
    max_positions = st.number_input("最多持股数", value=3, step=1)
    hold_days = st.number_input("最大持有天数", value=5, step=1)
    initial_capital = st.number_input("初始资金", value=1_000_000.0)

cfg = StrategyConfig(
    board_min_volume=board_min_volume,
    stock_float_cap_max=stock_float_cap_max,
    first_day_gain_pct=first_day_gain_pct,
    max_positions=max_positions,
    hold_days=hold_days,
)
service = TradingService(cfg)

col1, col2 = st.columns(2)
if col1.button("执行选股"):
    df = service.screen()
    st.subheader("候选股票")
    st.dataframe(df if not df.empty else pd.DataFrame())

if col2.button("执行回测"):
    result = service.backtest(initial_capital=initial_capital)
    st.subheader("回测结果")
    st.json(result)
    trades = pd.DataFrame(result.get("trades", []))
    if not trades.empty:
        st.dataframe(trades)
