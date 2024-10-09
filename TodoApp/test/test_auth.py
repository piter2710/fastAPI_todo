from .utils import *
from ..Router.auth import get_db,authenticate_user,create_access_token,SECRET_KEY,ALGORITHM,get_current_user
from jose import jwt
from datetime import timedelta
app.dependency_overrides[get_db] = override_get_db
from fastapi import HTTPException
import pytest
def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user( test_user.username, "1234",db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username
    assert authenticated_user.email == test_user.email
def test_authenticate_user_invalid(test_user):
    db = TestingSessionLocal()
    wrong_user = authenticate_user( "wrong_user", "1234",db)
    assert wrong_user is False
def test_authenticate_user_invalid_password(test_user):
    db = TestingSessionLocal()
    wrong_user = authenticate_user( test_user.username, "12324",db)
    assert wrong_user is False
def test_create_access_token(test_user):
    username = 'testuser'
    user_id=1
    role = 'user'
    expires = timedelta(days=1)

    token = create_access_token(username,user_id,role,expires)
    decoded_token = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM], options={'verify_signature': False})

    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role

@pytest.mark.asyncio
async def test_get_current_user(test_user):
    encode = {'sub': 'testuser', 'id': 1, 'role': 'admin'}

    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    user = await get_current_user(token=token)
    assert user == {'username':'testuser','id':1,'user_role':'admin'}
@pytest.mark.asyncio
async def test_get_current_user_invalid(test_user):
    encode = {'role':'user'}
    token = jwt.encode(encode,SECRET_KEY,ALGORITHM)
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token=token)

    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == 'Could not validate user.'


