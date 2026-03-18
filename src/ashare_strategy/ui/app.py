from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from ashare_strategy.core.config import StrategyConfig
from ashare_strategy.execution.portfolio import TradingService
from ashare_strategy.utils import result_to_dataframes

st.set_page_config(page_title="A股策略工具", layout="wide")
st.title("A股选股与回测工具")

with st.sidebar:
    st.header("参数")
    board_min_volume = st.number_input("板块近5日最小成交量", value=120.0)
    stock_float_cap_max = st.number_input("流通A股上限", value=1_000_000_000.0)
    first_day_gain_pct = st.number_input("首日涨幅阈值(%)", value=7.0)
    max_positions = st.number_input("最多持股数", value=3, step=1)
    hold_days = st.number_input("最大持有天数", value=5, step=1)
    lookback_days = st.number_input("回测天数", value=365, step=10)
    rebalance_interval = st.number_input("调仓周期", value=7, step=1)
    initial_capital = st.number_input("初始资金", value=1_000_000.0)
    use_cache = st.checkbox("启用缓存", value=True)

cfg = StrategyConfig(
    board_min_volume=board_min_volume,
    stock_float_cap_max=stock_float_cap_max,
    first_day_gain_pct=first_day_gain_pct,
    max_positions=max_positions,
    hold_days=hold_days,
    lookback_days=lookback_days,
    rebalance_interval=rebalance_interval,
    use_cache=use_cache,
)
service = TradingService(cfg)

col1, col2 = st.columns(2)
if col1.button("执行选股"):
    df = service.screen()
    st.subheader("候选股票")
    st.dataframe(df if not df.empty else pd.DataFrame(), use_container_width=True)

if col2.button("执行回测"):
    result = service.backtest(initial_capital=initial_capital, mode="rolling")
    st.subheader("回测结果")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("策略收益", f"{result.get('strategy_return', 0):.2%}")
    m2.metric("基准收益", f"{result.get('benchmark_return', 0):.2%}")
    m3.metric("超额收益", f"{result.get('excess_return', 0):.2%}")
    m4.metric("最大回撤", f"{result.get('max_drawdown', 0):.2%}")

    candidates, trades, equity = result_to_dataframes(result)
    if not equity.empty:
        fig = px.line(equity, x="date", y="equity", title="策略净值曲线")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("候选股票")
    st.dataframe(candidates, use_container_width=True)
    st.subheader("交易记录")
    st.dataframe(trades, use_container_width=True)
