from ashare_strategy.data.health import ProviderHealthCheck


def test_health_to_dict_defaults_checks():
    health = ProviderHealthCheck(provider='akshare')
    payload = health.to_dict()
    assert payload['provider'] == 'akshare'
    assert payload['checks'] == []
