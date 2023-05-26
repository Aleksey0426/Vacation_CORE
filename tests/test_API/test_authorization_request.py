import pytest
import requests


# def test_auth_request(get_new_token_collaborator):
#     # username = 'aleksey.chugunov@irlix.ru'
#     # password = 'irlix2023'
#     request = get_new_token_collaborator
#     # print("Number 1", token_collaborator)
#     assert token_collaborator is not None

@pytest.mark.usefixtures('get_new_token_collaborator')
class TestAuth:
    def test_status_code(self, get_new_token_collaborator):
        request = get_new_token_collaborator
        # print("Number 2", token_collaborator)
        assert request.status_code is 200

    def test_access_token(self, get_new_token_collaborator):
        request = get_new_token_collaborator
        response = request.json()
        assert response['access_token'] is not None

    def test_refresh_token(self, get_new_token_collaborator):
        request = get_new_token_collaborator
        response = request.json()
        assert response['refresh_token'] is not None

    def test_expires_in(self, get_new_token_collaborator):
        request = get_new_token_collaborator
        response = request.json()
        assert response['expires_in'] == 1800

