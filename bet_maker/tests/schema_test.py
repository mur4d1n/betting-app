import pytest

from decimal import Decimal
from pydantic import ValidationError

from bet_maker.schemas import PostBetSchema


@pytest.mark.parametrize("valid_input", [
    {"event_id": 1, "bet_sum": Decimal("10.00")},
    {"event_id": "2", "bet_sum": Decimal("0.01")},
    {"event_id": 3, "bet_sum": Decimal("999.99")},
    # {"event_id": "abc", "bet_sum": Decimal("10.00")},
])
def test_valid_schema(valid_input):
    result = PostBetSchema(**valid_input)

    assert result.bet_sum == valid_input["bet_sum"]
    assert result.event_id == valid_input["event_id"]


@pytest.mark.parametrize("invalid_input", [
    {"event_id": 1, "bet_sum": 10},
    {"event_id": 1, "bet_sum": 5.5},
    {"event_id": 1, "bet_sum": Decimal("10")},
    {"event_id": 1, "bet_sum": Decimal("3.141")},
    {"event_id": 1, "bet_sum": Decimal("0.00")},
    {"event_id": 1, "bet_sum": Decimal("-1.12")},
    {"event_id": 1.1, "bet_sum": Decimal("10.00")},
    {"event_id": [1, 2, 3], "bet_sum": Decimal("10.00")},
    {"event_id": {"1": 2}, "bet_sum": Decimal("10.00")},
    # {"event_id": "abc", "bet_sum": Decimal("10.00")},
])
def test_invalid_schema(invalid_input):
    with pytest.raises(ValidationError):
        PostBetSchema(**invalid_input)
