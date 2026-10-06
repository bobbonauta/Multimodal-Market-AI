import pytest

from multimodal_market_ai.metrics import evaluate_r_multiples


def test_asymmetric_payoff_can_be_profitable_below_50_percent_wins() -> None:
    metrics = evaluate_r_multiples([2.0] * 49 + [-1.0] * 51)

    assert metrics["win_rate"] == pytest.approx(0.49)
    assert metrics["expectancy_r"] == pytest.approx(0.47)
    assert metrics["profit_factor"] == pytest.approx(98 / 51)


def test_empty_series_is_rejected() -> None:
    with pytest.raises(ValueError):
        evaluate_r_multiples([])
