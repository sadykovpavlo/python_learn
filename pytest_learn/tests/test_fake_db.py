import pytest

@pytest.mark.db
def test_insert_dict_to_fake_bd(db):
    test_dict = {'1': 'test'}
    db.insert(test_dict)
    assert db.rows ==  [{'1': 'test'}]

@pytest.mark.db
def test_sedded_fake_db_inserted_2_row(seeded_fake_db):
    assert seeded_fake_db.rows == [{"id": 1, "name": "alice"},{"id": 2, "name": "bob"}]
