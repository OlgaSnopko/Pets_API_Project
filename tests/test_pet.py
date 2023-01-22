import pytest
from api import Pets

pt = Pets()


def test_get_registered_and_delete():
    status = pt.get_registered_and_delete()
    assert status == 200


def test_get_token():
    token = pt.get_token()[0]
    status = pt.get_token()[3]
    assert token
    assert status == 200


def test_get_list_users():
    status = pt.get_list_users()[0]
    my_id = pt.get_list_users()[1]
    assert status == 200
    assert my_id


def test_get_pet():
    pet_id = pt.get_pet()[0]
    status = pt.get_pet()[1]
    assert pet_id
    assert status == 200


def test_get_pet_photo():
    status = pt.get_pet_photo()[0]
    assert status == 200


@pytest.mark.xfail
def test_get_pet_like():
    status = pt.get_pet_like()
    assert status == 200


def test_get_pet_like_save_pet():
    status = pt.get_pet_like_save_pet()
    assert status == 200


def test_add_pet_like():
    status = pt.add_pet_like()
    assert status == 200


def test_add_pet_comment():
    status = pt.add_pet_comment()[0]
    id_comment = pt.add_pet_comment()[1]
    assert status == 200
    assert id_comment


def test_get_pet_id():
    status = pt.get_pet_id()[0]
    id_pet = pt.get_pet_id()[1]
    name_pet = pt.get_pet_id()[2]
    gender = pt.get_pet_id()[3]
    owner_id = pt.get_pet_id()[4]
    type_pet = pt.get_pet_id()[1]
    assert status
    assert id_pet
    assert name_pet
    assert gender
    assert owner_id
    assert type_pet
