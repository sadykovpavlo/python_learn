import pytest
from practice_e import (
    unique_tags,
    most_common_status,
    all_paid,
    any_refunded,
    richest,
    numbered_titles,
    names_to_scores,
    running_total,
)


# ─────────────────────────────────────────────────────────────
# 1. unique_tags(raws: list[str]) -> list[str]
#    lower + dedup + sorted.  ['Py','api','py','API'] -> ['api','py']
#    Придумай: positive, edge (пустой вход), negative (unique_tags(5) -> TypeError).
# ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("entered_list, expectation", [
    pytest.param(['Py','api','py','API'], ['api', 'py'], id="valid positive case"),
    pytest.param([], [], id="edge empty_list"),
    pytest.param(['@','@','%','#'], ['#', '%', '@'], id="edge symbols"),
    pytest.param(['','',''], [''], id="edge empty str"),
])
def test_unique_tags(entered_list, expectation):
    result = unique_tags(entered_list)
    assert result == expectation

def test_unique_tags_negative():
    with pytest.raises(TypeError):
        unique_tags(1)


# ─────────────────────────────────────────────────────────────
# 2. most_common_status(tickets) -> str    (самый частый status)
# ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("entered_object, expected",[
    pytest.param([{"name": "Alice", "status": "active"}, {"name": "Bob", "status": "active"}, {"name": "Jemes", "status": "deactivate"}], "active", id="positive entered valid dict 3 odbjects"),
    pytest.param([{"name": "Jemes", "status": "deactivate"}], "deactivate", id="positive entered valid dict 1 odbjects"),
    pytest.param([], "", id="edge empty list expected result = empty str"),
    pytest.param([{"name": "Alice", "status": "active"}, {"name": "Bob", "status": "active"}], "active", id="edge same status")



])
def test_most_common_status(entered_object, expected):
    result = most_common_status(entered_object)
    assert result == expected

@pytest.mark.parametrize("entered_object, exeption", [
    pytest.param(1, TypeError,  id="negative TypeError expected"),
    pytest.param([], IndexError, id="negative IndexError expected")
])
def test_negative_most_coomon_status(entered_object, exeption):
    with pytest.raises(exeption):
        most_common_status(entered_object)
# ─────────────────────────────────────────────────────────────
# 3. all_paid(orders) -> bool  /  4. any_refunded(orders) -> bool
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# 5. richest(orders) -> str    (имя с макс. amount)
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# 6. numbered_titles(titles) -> list[str]   ['a','b'] -> ['1. a','2. b']
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# 7. names_to_scores(names, scores) -> dict
# ─────────────────────────────────────────────────────────────


# ─────────────────────────────────────────────────────────────
# 8. running_total(nums) -> генератор   [1,2,3] -> 1,3,6
#    Помни: это генератор, результат надо list(...) прогнать.
# ─────────────────────────────────────────────────────────────
