import pytest
from practice import count_by_status, parse_tags, classify_age, enrich_user
from pytest_mock import MockerFixture

@pytest.mark.parametrize("entered_list, expected_dict",[
   pytest.param([{'id':1,'status':'open'}, {'id':2,'status':'open'}, {'id':3,'status':'closed'}], {'open': 2, 'closed': 1}, id="positive"),
    pytest.param([{'id':1,'status':'open'}, {'id':1,'status':'open'}], {'open': 2}, id="edge_same_id"),
    
])
def test_count_by_status_positive(entered_list, expected_dict):
    result = count_by_status(entered_list)
    assert result == expected_dict

@pytest.mark.parametrize("bad_ticets", [
    pytest.param([{}], id="edge_empty_dict"),
    pytest.param([{"1":"1"}], id="negative_wrong_key")
])
def test_count_by_status_negative(bad_ticets):
    with pytest.raises(KeyError):
        count_by_status(bad_ticets)

@pytest.mark.parametrize("incom_str, expected", [
    pytest.param("Test1, Test2", ["test1", "test2"], id= "positive 2 words income"),
    pytest.param("Test1", ["test1"], id= "positive 1 word income"),
    pytest.param("1111", ["1111"], id= "positive nums"),
    pytest.param("11  ,  ,  11", ["11", "11"], id= "positive nums and comma and space"),
    pytest.param("&&&&, @@@@@, ****", ["&&&&", "@@@@@", "****"], id= "edge case some symbols" ),
    pytest.param("", [], id= "edge case empty str" ),
    pytest.param(",,,,,,", [], id= "edge case empty only commas" )
])
def test_parse_tags_positive(incom_str, expected):
    result = parse_tags(incom_str)
    assert result == expected

@pytest.mark.parametrize("income_not_str", [
    ({"test": "test"}),
    (99),
    (45.2)
])
def test_parse_tags_negative(income_not_str):
    with pytest.raises(AttributeError):
        parse_tags(income_not_str)

@pytest.mark.parametrize("entered_age, expected_response",[
    (0, "minor"),
    (1, "minor"),
    (12.5, "minor"),
    (17, "minor"),
    (18, "adult"),
    (28, "adult"),
    (64, "adult"),
    (65, "senior"),
    (149, "senior"),
    (150, "senior")
])
def test_classify_age_positive(entered_age, expected_response):
    result = classify_age(entered_age)
    assert result == expected_response

@pytest.mark.parametrize("entered_age",[
    (-1),
    (151),
])
def test_classify_age_out_of_range(entered_age):
    with pytest.raises(ValueError, match=f'age out of range: {entered_age}'):
        classify_age(entered_age)

@pytest.mark.parametrize("not_int_given",[
    ([]),
    ('151')
])
def test_classify_age_not_int_given(not_int_given):
    with pytest.raises(TypeError):
        classify_age(not_int_given)


@pytest.mark.parametrize("valid_user_id, response", [
    pytest.param(1, {"id": 1, "status": "ok", "profile": {"name": "Alice"}}, id = "valid id num = 1"),
    pytest.param(1000, {"id": 1000, "status": "ok", "profile": {"name": "Alice"}}, id = "valid id num = 1000")
])
def test_enrich_user_positive(valid_user_id, response, mocker):
    mock = mocker.patch("practice.fetch_profile", return_value = {"name": "Alice"})
    result = enrich_user(valid_user_id)
    assert result == response
    mock.assert_called_once_with(valid_user_id)

@pytest.mark.parametrize("valid_user_id, response", [
    pytest.param('1', {"id": '1', "status": "ok", "profile": {"name": "Alice"}}, id = "edge id as str"),
    pytest.param(1.1, {"id": 1.1, "status": "ok", "profile": {"name": "Alice"}}, id = "edge id as float")
   
])
def test_enrich_user_edge(valid_user_id, response, mocker):
    mock = mocker.patch("practice.fetch_profile", return_value = {"name": "Alice"})
    result = enrich_user(valid_user_id)
    assert result == response
    mock.assert_called_once_with(valid_user_id)


def test_enrich_user_rise_timeout_error(mocker):
    mock = mocker.patch("practice.fetch_profile", side_effect = TimeoutError)
    result = enrich_user(1)
    assert result == {"id": 1, "status": "unavailable", "profile": None}
    mock.assert_called_once_with(1)
