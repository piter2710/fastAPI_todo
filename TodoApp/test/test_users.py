from .utils import *
from ..Router.users import get_current_user,get_db
from fastapi import status
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_get_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_user.username
    assert response.json()['email'] == test_user.email
    assert response.json()['id'] == test_user.id
    assert response.json()['is_active'] == test_user.is_active
    assert response.json()['role'] == test_user.role
    assert response.json()['phone_number'] == test_user.phone_number

def test_change_password(test_user):
    response = client.put('/user/password',json={
        "password":"1234",
        "new_password":"12345"
    })
    assert response.status_code == status.HTTP_204_NO_CONTENT
def test_change_password_fail(test_user):
    response = client.put('/user/password',json={
        "password":"321312",
        "new_password":"1234"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()=={'detail':'Incorrect current password'}
def test_change_phone_number_success(test_user):
    response = client.put("/user/phonenumber/2222222222")
    assert response.status_code == status.HTTP_204_NO_CONTENT