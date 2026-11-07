from module04_programming.week8_buggy import format_summary, get_total, is_over_limit


def test_get_total_correct():
    recs = [{"amount": 100}, {"amount": 200}]
    assert get_total(recs) == 300


def test_is_over_limit_true():
    assert is_over_limit(1500) is True


def test_is_over_limit_false():
    assert is_over_limit(500) is False


def test_is_over_limit_boundary():
    assert is_over_limit(1000) is False


def test_format_summary():
    assert format_summary(1234.56, 3) == "Total: $1234.56 across 3 records"
