from ashare_strategy.execution.state import PositionStore


def test_position_store(tmp_path):
    store = PositionStore(str(tmp_path / "positions.json"))
    payload = [{"stock_code": "000001", "shares": 100}]
    store.save(payload)
    assert store.load() == payload
