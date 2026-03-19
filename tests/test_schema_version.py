from ashare_strategy.utils import success_response


def test_success_response_has_schema_version():
    res = success_response({'ok': True})
    assert res['schema_version'] == '1.0'
    assert res['status'] == 'success'
